import os

def test_function():
    return True


def wait_for_and_execute_command(filename=None):
    if filename is None:
        while (True):
            inp = input('Enter a command or statement:\n')
            inp = inp.replace('\\n', '\n')
            # print(f'Executing: \n{inp}')
            try:
                exec(inp.encode(), globals())
            except Exception as e:
                ind = str(e).find('Stacktrace')
                if ind > 0:
                    print(str(e)[:ind])
                else:
                    print(e)
    else:
        with open('complete_code.py', 'w', encoding='utf-8') as f:
            f.write('')
        while (True):
            inp = input(f'Enter anything to execute file {os.getcwd()}/{filename}: ')
            excode = ''
            with open(filename, 'r', encoding='utf-8') as f:
                excode = f.read()
            with open('complete_code.py', 'a', encoding='utf-8') as f:
                f.write(excode + '\n')
            try:
                exec(excode.encode(), globals())
            except Exception as e:
                ind = str(e).find('Stacktrace')
                if ind > 0:
                    print(str(e)[:ind])
                else:
                    print(e)
