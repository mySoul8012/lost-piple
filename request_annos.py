from lost.pyapi import script
import os
import random

ENVS = ['lost']

ARGUMENTS = {
    'recursive': {
        'value': 'true',
        'help': 'Walk recursively through folder structure'
    },
    'valid_imgtypes': {
        'value': "['.jpg', '.jpeg', '.png', '.bmp']",
        'help': 'Image types for which annotations will be requested.'
    },
    'shuffle': {
        'value': 'false',
        'help': 'Shuffle images before requesting annotations.'
    }
}

class LostScript(script.Script):
    '''Request annotations for each image in an imageset.
    An imageset is basically a folder containing images.
    '''

    def check_and_request(self, fs, path):
        if fs.isfile(path):
            if os.path.splitext(path)[1].lower() in self.get_arg('valid_imgtypes'):
                self.outp.request_annos(path, fs=fs)
                self.logger.info(f'Requested annotations for: {path}')
            else:
                self.logger.warning(f'{path} is not a valid image file!')
        else:
            self.logger.warning(f'{path} is not a valid file!')

    def main(self):
        for ds in self.inp.datasources:
            media_path = ds.path
            fs = ds.get_fs()
            if self.get_arg('recursive') == 'true':
                for root, dirs, files in fs.walk(media_path):
                    for file in files:
                        self.check_and_request(fs, os.path.join(root, file))
            else:
                for file in fs.listdir(media_path):
                    self.check_and_request(fs, os.path.join(media_path, file))
            if self.get_arg('shuffle') == 'true':
                random.shuffle(self.outp.requests)
