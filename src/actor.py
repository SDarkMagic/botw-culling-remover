# Handles searching for and downloading images from google's API
import json
import random
import pathlib
from wildbits import _sarc
import oead
import aamp
import util

config = util.getConfigData()

class ActorPack:
    def __init__(self, file_path):
        self.path = pathlib.Path(file_path)
        self.pack, self.tree, self.moddedFiles = _sarc.open_sarc(self.path)

    def remove_culling(self):
        files = self.tree['Actor'].keys()
        attclientlist = None

        if ('AttClientList' in files):
            actor_path = f'Actor/AttClientList/{list((self.tree["Actor"]["AttClientList"]).keys())[0]}'
            attclientlist = _sarc.get_nested_file_data(self.pack, actor_path)

        if (attclientlist == None):
            return self.pack

        #att_clientlist_data = oead.aamp.ParameterIO.from_binary(attclientlist)
        att_clientlist_data = aamp.Reader(attclientlist).parse()
        listData = att_clientlist_data.list('param_root').list('AttClients')

        # item is a tuple containing an aamp.Name and the value for that given key.
        # This loop grabs the value from the aamp via the given key
        # and then performs various actions on it
        atts = {}
        for item in listData.objects.items():
            data = item[1] # Parameters in the final nested level of the object [Name, FileName]
            if (str(data.param('Name')) not in ['LockOn', 'AutoAim']):
                atts.update({item[0]: item[1]})
        att_clientlist_data.list('param_root').list('AttClients').objects = atts
        writer = aamp.Writer(att_clientlist_data)
        return _sarc.replace_file(self.pack, actor_path, bytes(writer.get_bytes()))

    def write(self, output):
        writer = oead.SarcWriter.from_sarc(self.remove_culling())
        with open(output, 'wb') as write_file:
            new_sarc = bytes(writer.write()[1])
            write_file.write(oead.yaz0.compress(new_sarc))




if __name__ == '__main__':
    actor = ActorPack(file_path="C:/Users/drago/Desktop/cullingToZero/assets/Enemy_Bokoblin_Gold.sbactorpack")
    actor.write()
