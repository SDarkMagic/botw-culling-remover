import pathlib
import time
import argparse
import util
import bfres
import colorama
import random
import json
import actor

colorama.init()

parser = argparse.ArgumentParser(description='A tool for enabling culling for all or a specific set of models and actors in botw.')
subparsers = parser.add_subparsers()

# Enable setting culling to true for all files that match the specified parameters
r_culling = subparsers.add_parser('enable', aliases=['e'])
r_culling.add_argument('-o', type=str, help='Location of the graphics pack to output the modified files to.', required=False, default=None, dest='output')
r_culling.add_argument('-sub', type=str, help='Substring to match agaist rather than processing all files', required=False, default=None, dest='sub_string')
parser.add_argument('game_dir', help='Directory containing the content folder for botw.', type=str)

def enable_all_culling(args):
    config = util.getConfigData()
    content = pathlib.Path(f"{args.game_dir}/content")
    actor_dir = content / 'Actor' / 'Pack'
    model_dir = content / 'Model'
    output = util.findMKDir(f'{args.output}/content')
    output_actor_dir = util.findMKDir(output / 'Actor' / 'Pack')

    # Check Actors
    print('Processing actorpacks...')
    for file in actor_dir.iterdir():
        if (not file.is_file()):
            continue
        if (args.sub_string != None):
            if (args.sub_string.lower() in file.name.lower().split('_')):
                actorpack = actor.ActorPack(file)
                actorpack.write(output_actor_dir / file.name)
            else:
                continue
        else:
            actorpack = actor.ActorPack(file)
            actorpack.write(output_actor_dir / file.name)

    print('Processing models...')
    for file in model_dir.iterdir():
        if (not file.is_file()):
            continue
        if (args.sub_string != None):
            if (args.sub_string.lower() in file.name.lower().split('_')):
                bfres.changeCulling(file, output)
            else:
                continue
        else:
            bfres.changeCulling(file, output)

    return

def randomizeAll(args):
    enable_all_culling(args)
    return

r_culling.set_defaults(func=randomizeAll)

if __name__ == '__main__':
    args = parser.parse_args()
    args.func(args)
    colorama.deinit()