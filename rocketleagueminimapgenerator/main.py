import argparse
import os
import time

from rocketleagueminimapgenerator.data.actor_data import parse_actor_data
from rocketleagueminimapgenerator.data.data import load_data, \
    set_data_start, set_data_end
from rocketleagueminimapgenerator.data.object_numbers import \
    parse_ball_obj_nums, parse_car_obj_nums, parse_player_info, get_player_info
from rocketleagueminimapgenerator.parser.frames import load_frames
from rocketleagueminimapgenerator.render.minimap import render_field
from rocketleagueminimapgenerator.render.player_data_full import \
    render_player_data_full
from rocketleagueminimapgenerator.render.transcode import render_video
from rocketleagueminimapgenerator.util.data_explorer import data_explorer_cli

with open(os.path.join('assets', 'field-template.svg'), 'r') as svg_file:
    field_template = svg_file.read()

with open(os.path.join('assets', 'player-data-full-template.svg'),
          'r') as svg_file:
    player_data_full_template = svg_file.read()

car_template = '<circle class="team{team_id} stroke-black" ' \
               'cx="{car_pos_x}" cy="{car_pos_y}" r="{car_size}"/>' \
               '<polygon class="team{team_id} stroke-black" ' \
               'points="' \
               '{car_triangle_pt1_x},{car_triangle_pt1_y} ' \
               '{car_triangle_pt2_x},{car_triangle_pt2_y} ' \
               '{car_triangle_pt3_x},{car_triangle_pt3_y} " ' \
               'transform="rotate({car_angle} {car_pos_x} {car_pos_y})' \
               'translate(0 -{arrow_move})"/>'
frame_num_format = '{0:04d}'


def main():
    parser = argparse.ArgumentParser(prog='rocketleagueminimapgenerator')

    # Required args
    parser.add_argument('game_json', help='The name of the game json.')

    parser.add_argument('--process_type',
                        choices=['video_minimap',
                                 'video_player_data',
                                 'data_explorer'],
                        default='video_minimap')

    # Optional args
    parser.add_argument('--data_start',
                        help='Number of frames to render (start).',
                        type=int)
    parser.add_argument('--data_end',
                        help='Number of frames to render (end).',
                        type=int)

    args = parser.parse_args()

    out_prefix = args.game_json

    load_data(out_prefix)
    parse_actor_data()
    parse_ball_obj_nums()
    parse_car_obj_nums()
    parse_player_info()
    load_frames()

    video_prefix = os.path.join('renders', out_prefix.split('.')[0])
    if args.data_start:
        set_data_start(args.data_start)
    if args.data_end:
        set_data_end(args.data_end)

    if args.process_type == 'video_minimap':
        print('Creating video of minimap')

        video_prefix = os.path.join('renders', out_prefix.split('.')[0])
        render_field(video_prefix)
        render_video(video_prefix, 'minimap')
    elif args.process_type == 'video_player_data':
        render_player_data_full(video_prefix)
        for player_id in get_player_info().keys():
            render_video(video_prefix,
                         os.path.join('player-data', str(player_id)))
    elif args.process_type == 'data_explorer':
        time.sleep(.5)
        data_explorer_cli()
    else:
        print('Unexpected Argument Error:',
              'process_type is', args.process_type)


if __name__ == "__main__":
    main()
