#!/usr/bin/env python3
import sys
import time
import json
from queue import Empty
from pprint import pprint
from stdio_ipc import ChildProcess

def action(ai):
    try:
        ai.send('action\n')
        message = ai.recv(timeout=1) # timeout after 1s
        say, hand = map(int, message.split(' '))
    except Empty as e:
        return { 'err': 'timeout' }
    except:
        return { 'err': 'wrong format. your output: %s' % repr(message) }
    return { 'say': say, 'hand': hand }

def message(ai, id, res):
    ai.send('message\n%d %d %d\n' % (id, res['say'], res['hand']))

def send_id(ai, id):
    ai.send('id\n%d\n' % id)

def check_both(ai1_success, ai2_success, res1, res2):
    if not ai1_success and not ai2_success:
        finish(0, res1['err'], res2['err'])
    elif not ai1_success and ai2_success:
        finish(2, res1['err'], '')
    elif not ai2_success and ai1_success:
        finish(1, '', res2['err'])

def finish(winner, err1, err2):
    # kill ai and write stdio log
    if type(ai1) is not dict:
        ai1.exit()
    if type(ai2) is not dict:
        ai2.exit()

    # write result
    result = {
        'ai1_id': id1,
        'ai2_id': id2,
        'ai1_err': err1,
        'ai2_err': err2,
        'winner': winner,
    }
    pprint(result)
    with open('result.json', 'w') as f:
        f.write(json.dumps(result))

    # exit
    sys.exit(0)

def spawnAI(args, save_stdin_path, save_stdout_path, save_stderr_path):
    try:
        ai = ChildProcess(args, save_stdin_path, save_stdout_path, save_stderr_path)
        return ai
    except:
        return { 'err': 'fail to spawn the program.' + str(sys.exc_info()[1]) }


if len(sys.argv) != 3:
    print('usage:   ./sample_judge.py AI1Path AI2Path')
    print('example: ./sample_judge.py ./sample_ai ./sample_ai')
    print('')
    sys.exit(1)

# run ai
seed_base = int(time.time() * 1e3) % 10000000000
id1 = seed_base % 2
id2 = 1 - id1
ai1 = spawnAI([sys.argv[1], '%.0f' % (seed_base+0)], 'ai1_stdin.log', 'ai1_stdout.log', 'ai1_stderr.log')
ai2 = spawnAI([sys.argv[2], '%.0f' % (seed_base+1)], 'ai2_stdin.log', 'ai2_stdout.log', 'ai2_stderr.log')
check_both(type(ai1) is not dict, type(ai2) is not dict, ai1, ai2)

# send id
send_id(ai1, id1)
send_id(ai2, id2)


while True:
    # action
    res1 = action(ai1)
    res2 = action(ai2)
    check_both('err' not in res1, 'err' not in res2, res1, res2)

    # judge
    ai1_correct = res1['hand'] + res2['hand'] == res1['say']
    ai2_correct = res1['hand'] + res2['hand'] == res2['say']
    if ai1_correct != ai2_correct:
        finish(1 if ai1_correct else 2, '', '')

    # broadcast history
    message(ai1, id1, res1)
    message(ai1, id2, res2)
    message(ai2, id1, res1)
    message(ai2, id2, res2)
