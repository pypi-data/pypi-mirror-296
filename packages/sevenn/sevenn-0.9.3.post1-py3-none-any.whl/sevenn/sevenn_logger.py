import os
import traceback
from datetime import datetime

from ase.data import atomic_numbers

import sevenn._const
import sevenn._keys as KEY

CHEM_SYMBOLS = {v: k for k, v in atomic_numbers.items()}


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(
                *args, **kwargs
            )
        return cls._instances[cls]


class Logger(metaclass=Singleton):

    SCREEN_WIDTH = 120  # half size of my screen / changed due to stress output

    def __init__(
        self, filename: str = 'log.sevenn', screen: bool = False, rank: int = 0
    ):
        self.rank = rank
        if rank == 0:
            self.logfile = open(filename, 'w', buffering=1)
            self.files = {}
            self.screen = screen
        else:
            self.logfile = None
            self.screen = False
        self.timer_dct = {}
        # self.logfile = open(filename, 'w', buffering=1)
        # self.screen = screen
        # self.timer_dct = {}

    def __del__(self):
        if self.logfile is not None:
            self.logfile.close()
        for f in self.files.values():
            f.close()

    def write(self, content: str):
        # no newline!
        if self.logfile is not None:
            self.logfile.write(content)
            if self.screen:
                print(content, end='')
        else:
            pass

    def writeline(self, content: str):
        content = content + '\n'
        self.write(content)

    def init_csv(self, filename: str, header: list):
        if self.rank == 0:
            self.files[filename] = open(filename, 'w', buffering=1)
            self.files[filename].write(','.join(header) + '\n')
        else:
            pass

    def append_csv(self, filename: str, content: list, decimal: int = 6):
        if self.rank == 0:
            if filename not in self.files:
                self.files[filename] = open(filename, 'a', buffering=1)
            str_content = []
            for c in content:
                if isinstance(c, float):
                    str_content.append(f'{c:.{decimal}f}')
                else:
                    str_content.append(str(c))
            self.files[filename].write(','.join(str_content) + '\n')
        else:
            pass

    def natoms_write(self, natoms):
        content = ''
        total_natom = {}
        for label, natom in natoms.items():
            content += self.format_k_v(label, natom)
            for specie, num in natom.items():
                try:
                    total_natom[specie] += num
                except KeyError:
                    total_natom[specie] = num
        content += self.format_k_v('Total, label wise', total_natom)
        content += self.format_k_v('Total', sum(total_natom.values()))
        self.write(content)

    def statistic_write(self, statistic: dict):
        content = ''
        for label, dct in statistic.items():
            dct_new = {}
            for k, v in dct.items():
                dct_new[k] = f'{v:.3f}'
            content += self.format_k_v(label, dct_new)
        self.write(content)

    def epoch_write_train_loss(self, loss):
        content = ''
        for label, val in loss.items():
            content += self.format_k_v(str(label), f'{val:.6f}')
        content += self.format_k_v('Total loss', f'{sum(loss.values()):.6f}')
        self.write(content)

    # TODO : refactoring!!!, this is not loss, rmse
    def epoch_write_specie_wise_loss(self, train_loss, valid_loss):
        lb_pad = 21
        fs = 6
        pad = 21 - fs
        ln = '-' * fs
        total_atom_type = train_loss.keys()
        content = ''

        for at in total_atom_type:
            t_F = train_loss[at]
            v_F = valid_loss[at]
            at_sym = CHEM_SYMBOLS[at]
            content += (
                '{label:{lb_pad}}{t_E:<{pad}.{fs}s}{v_E:<{pad}.{fs}s}'.format(
                    label=at_sym, t_E=ln, v_E=ln, lb_pad=lb_pad, pad=pad, fs=fs
                )
                + '{t_F:<{pad}.{fs}f}{v_F:<{pad}.{fs}f}'.format(
                    t_F=t_F, v_F=v_F, pad=pad, fs=fs
                )
            )
            content += '{t_S:<{pad}.{fs}s}{v_S:<{pad}.{fs}s}'.format(
                t_S=ln, v_S=ln, pad=pad, fs=fs
            )
            content += '\n'
        self.write(content)

    @staticmethod
    def write_table(dct):
        keys = list(dct.keys())
        values = [f'{dct[key]:.6f}' for key in keys]

        # Calculate padding
        padding = [max(len(k), len(v)) + 2 for k, v in zip(keys, values)]

        # Create the key and value rows
        key_row = '|'.join(key.center(pad) for key, pad in zip(keys, padding))
        value_row = '|'.join(
            value.rjust(pad) for value, pad in zip(values, padding)
        )

        # Create separator
        separator = '-' * sum(padding) + '-' * (len(padding) - 1)

        # Print the table
        Logger().writeline(key_row)
        Logger().writeline(separator)
        Logger().writeline(value_row)
        Logger().writeline(separator)

    @staticmethod
    def write_full_table(dict_list, row_labels, decimal_places=6, pad=2):
        """
        Assume data_list is list of dict with same keys
        """
        assert len(dict_list) == len(row_labels)
        label_len = max(map(len, row_labels))
        # Extract the column names and create a 2D array of values
        col_names = list(dict_list[0].keys())

        values = [list(d.values()) for d in dict_list]

        # Format the numbers with the given decimal places
        formatted_values = [
            [f'{value:.{decimal_places}f}' for value in row] for row in values
        ]

        # Calculate padding lengths for each column (with extra padding)
        max_col_lengths = [
            max(len(str(value)) for value in col) + pad
            for col in zip(col_names, *formatted_values)
        ]

        # Create header row and separator
        header = ' ' * (label_len + pad) + ' '.join(
            col_name.ljust(pad)
            for col_name, pad in zip(col_names, max_col_lengths)
        )
        separator = '-'.join('-' * pad for pad in max_col_lengths) + '-' * (
            label_len + pad
        )

        # Print header and separator
        Logger().writeline(header)
        Logger().writeline(separator)

        # Print the data rows with row labels
        for row_label, row in zip(row_labels, formatted_values):
            data_row = ' '.join(
                value.rjust(pad) for value, pad in zip(row, max_col_lengths)
            )
            Logger().writeline(f'{row_label.ljust(label_len)}{data_row}')

    @staticmethod
    def format_k_v(key, val, write=False):
        MAX_KEY_SIZE = 20
        SPERATOR = ', '
        EMPTY_PADDING = ' ' * (MAX_KEY_SIZE + 3)
        NEW_LINE_LEN = Logger.SCREEN_WIDTH - 5
        val = str(val)
        content = f'{key:<{MAX_KEY_SIZE}}: {val}'
        if len(content) > NEW_LINE_LEN:
            content = f'{key:<{MAX_KEY_SIZE}}: '
            # sperate val by sperator
            val_list = val.split(SPERATOR)
            current_len = len(content)
            for val_compo in val_list:
                current_len += len(val_compo)
                if current_len > NEW_LINE_LEN:
                    newline_content = f'{EMPTY_PADDING}{val_compo}{SPERATOR}'
                    content += f'\\\n{newline_content}'
                    current_len = len(newline_content)
                else:
                    content += f'{val_compo}{SPERATOR}'

        if content.endswith(f'{SPERATOR}'):
            content = content[: -len(SPERATOR)]
        content += '\n'

        if write is False:
            return content
        else:
            Logger().write(content)
            return ''

    def greeting(self):
        LOGO_ASCII_FILE = f'{os.path.dirname(__file__)}/logo_ascii'
        with open(LOGO_ASCII_FILE, 'r') as logo_f:
            logo_ascii = logo_f.read()
        content = 'SEVENN: Scalable EquVariance-Enabled Neural Network\n'
        content += f'sevenn version {sevenn._const.SEVENN_VERSION}\n'
        content += 'reading yaml config...'
        self.write(content)
        self.write(logo_ascii)

    def bar(self):
        content = '-' * Logger.SCREEN_WIDTH + '\n'
        self.write(content)

    def print_config(self, model_config, data_config, train_config):
        """
        print some important information from config
        """
        content = (
            'succesfully read yaml config!\n\n' + 'from model configuration\n'
        )
        for k, v in model_config.items():
            content += Logger.format_k_v(k, v)
        content += '\nfrom train configuration\n'
        for k, v in train_config.items():
            content += Logger.format_k_v(k, v)
        content += '\nfrom data configuration\n'
        for k, v in data_config.items():
            content += Logger.format_k_v(k, v)
        self.write(content)

    # TODO: This is not good make own exception
    def error(self, e: Exception):
        content = ''
        if type(e) is ValueError:
            content += 'Error occured!\n'
            content += str(e) + '\n'
        else:
            content += 'Unknown error occured!\n'
            content += traceback.format_exc()
        self.write(content)

    def timer_start(self, name: str):
        self.timer_dct[name] = datetime.now()

    def timer_end(self, name: str, message: str, remove=True):
        """
        print f"{message}: {elapsed}"
        """
        elapsed = str(datetime.now() - self.timer_dct[name])
        # elapsed = elapsed.strftime('%H-%M-%S')
        if remove:
            del self.timer_dct[name]
        self.write(f'{message}: {elapsed[:-4]}\n')

    def dict_of_counter(self, counter_dict):
        # Find the Counter with the most keys and use it as a reference
        ref_counter = max(counter_dict.values(), key=lambda x: len(x))

        # Find the longest name and value length for formatting
        max_name_length = max(len(name) for name in counter_dict.keys())
        max_value_length = max(
            len(str(value))
            for counter in counter_dict.values()
            for value in counter.values()
        )

        # Create the header
        header_parts = ['Name'.ljust(max_name_length)] + [
            key.rjust(max_value_length) for key in ref_counter.keys()
        ]
        header = ' '.join(header_parts)
        table_output = [header, '-' * len(header)]

        # Create each row
        for name, counter in counter_dict.items():
            row_parts = [name.ljust(max_name_length)] + [
                str(counter.get(key, '')).rjust(max_value_length)
                for key in ref_counter.keys()
            ]
            table_output.append(' '.join(row_parts))

        self.writeline('\n'.join(table_output))

    # TODO: print it without config
    # TODO: refactoring, readout part name :(
    def print_model_info(self, model, config):
        from functools import partial

        kv_write = partial(self.format_k_v, write=True)
        self.writeline('Irreps of features')
        kv_write(
            'edge_feature', model.get_irreps_in('edge_embedding', 'irreps_out')
        )
        for i in range(config[KEY.NUM_CONVOLUTION]):
            kv_write(
                f'{i}th node',
                model.get_irreps_in(f'{i}_self_interaction_1'),
            )
        kv_write(
            'readout irreps',
            model.get_irreps_in(f'{i}_equivariant_gate', 'irreps_out'),
        )

        num_weights = sum(
            p.numel() for p in model.parameters() if p.requires_grad
        )
        self.writeline(f'Total number of weight in model is {num_weights}\n')
