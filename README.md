# py-stdio-ipc

Python IPC based on stdin / stdout

## Example

Usage: `./sample_judge.py AI1Path AI2Path`

    $ clang++ -Wall sample_ai_stderr.cc -o sample_ai_stderr
    $ clang++ -Wall sample_ai_tle.cc -o sample_ai_tle
    $ clang++ -Wall sample_ai_re.cc -o sample_ai_re
    $ clang++ -Wall sample_ai.cc -o sample_ai
    $ clang++ -Wall bad1.cc -o bad1
    $ clang++ -Wall bad2.cc -o bad2
      
    $ ./sample_judge.py ./sample_ai ./sample_ai
    {'ai1_err': '', 'ai1_id': 0, 'ai2_err': '', 'ai2_id': 1, 'winner': 2}
     
    $ ./sample_judge.py ./sample_ai ./sample_stderr
    {'ai1_err': '', 'ai1_id': 0, 'ai2_err': '', 'ai2_id': 1, 'winner': 1}
      
    $ ./sample_judge.py ./sample_ai ./sample_tle
    {'ai1_err': '', 'ai1_id': 0, 'ai2_err': 'timeout', 'ai2_id': 1, 'winner': 1}
      
    $ ./sample_judge.py ./sample_ai ./sample_re
    {'ai1_err': '',
     'ai1_id': 1,
     'ai2_err': "wrong format. your output: ''",
     'ai2_id': 0,
     'winner': 1}

    $ ./sample_judge.py ./sample_ai ./bad1
    {'ai1_err': '', 'ai1_id': 1, 'ai2_err': 'timeout', 'ai2_id': 0, 'winner': 1}

    $ ./sample_judge.py ./sample_ai ./bad2
    {'ai1_err': '',
     'ai1_id': 1,
     'ai2_err': 'fail to send id. program unexpectedly terminated',
     'ai2_id': 0,
     'winner': 1}

## API

All of the following APIs will block the main thread. See `sample_judge.py` and `sample_ai.cc` to know how to use them.

### stdio\_ipc.ChildProcess(args, save\_stdin\_path, save\_stdout\_path, save\_stderr\_path)

Create a child process with program arguments `args`. Save stdio into files.

### stdio\_ipc.ChildProcess.send(content)

Send `content` to the child process. **`content` MUST ends with `\n`**.

### stdio\_ipc.ChildProcess.recv(timeout)

Receive output from the child process. Timeout if not response correctly with `timeout` second(s). **The output of child process MUST ends with `END\n` and remember to `flush`**, otherwise it may timeout.

### stdio\_ipc.ChildProcess.exit()

Kill the child.

### (Deprecated) ~~stdio\_ipc.ChildProcess.save\_stdio(path\_stdin, path\_stdout, path\_stderr)~~

~~Save the stdio history to `path_stdin`, `path_stdout` and `path_stderr` respectively. `END\n` will be removed from the result of `stdout`.~~

## About the example

I wrote an example to show how to use the library. The example is an AI game of two players. Each player shows a number (0 ~ 5) using his fingers while yell another number (0 ~ 10) at the same time. Somebody wins if what he yelled equals to the sum of what both of the two showed in hands.

- `sample_judge.py` shows how can a judge program be written, using this library.
- `sample_ai.cc` shows how should a player communicate with the judge. Note the `end()` function.
- `sample_ai_tle.cc` and `sample_ai_re.cc` are both used to demonstrate what will happen if a player program misbehave.
- `sample_ai_stderr.cc` is a program that prints much log into stderr.
