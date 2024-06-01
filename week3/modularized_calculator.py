#! /usr/bin/python3

def read_number(line, index):
    number = 0
    while index < len(line) and line[index].isdigit():
        number = number * 10 + int(line[index])
        index += 1
    if index < len(line) and line[index] == '.':
        index += 1
        decimal = 0.1
        while index < len(line) and line[index].isdigit():
            number += int(line[index]) * decimal
            decimal /= 10
            index += 1
    token = {'type': 'NUMBER', 'number': number}
    return token, index


def read_plus(line, index):
    token = {'type': 'PLUS'}
    return token, index + 1


def read_minus(line, index):
    token = {'type': 'MINUS'}
    return token, index + 1

# 掛け算と割り算のトークンを追加
def read_multiply(line, index):
    token = {'type': 'MULTIPLY'}
    return token, index + 1

def read_divide(line, index):
    token = {'type': 'DIVIDE'}
    return token, index + 1

# 括弧のトークンを追加

def read_first_bracket(line, index):
    token = {'type': 'LPAREN'}
    return token, index + 1

def read_end_bracket(line, index):
    token = {'type': 'RPAREN'}
    return token, index + 1


def tokenize(line):
    tokens = []
    index = 0
    while index < len(line):
        if line[index].isdigit():
            (token, index) = read_number(line, index)
        elif line[index] == '+':
            (token, index) = read_plus(line, index)
        elif line[index] == '-':
            (token, index) = read_minus(line, index)
            # 掛け算と割り算の追加
        elif line[index] == '*':
            (token, index) = read_multiply(line, index)
        elif line[index] == '/':
            (token, index) = read_divide(line, index)
            # 括弧の追加
        elif line[index] == '(':
            (token, index) = read_first_bracket(line, index)
        elif line[index] == ')':
            (token, index) = read_end_bracket(line, index)
        else:
            print('Invalid character found: ' + line[index])
            exit(1)
        tokens.append(token)
    return tokens


# 中身もモジュール化

def evaluate(tokens):
    # 括弧の処理
    index = 0
    while index < len(tokens):
        if tokens[index]['type'] == 'LPAREN':
            # Find the matching right parenthesis
            balance = 0
            for look_ahead_index in range(index, len(tokens)):
                if tokens[look_ahead_index]['type'] == 'LPAREN':
                    balance += 1
                elif tokens[look_ahead_index]['type'] == 'RPAREN':
                    balance -= 1
                    if balance == 0:
                        break
            else:
                print('No matching right parenthesis')
                exit(1)
            # Recursively evaluate the expression inside the parenthesis
            inner_answer = evaluate(tokens[index + 1:look_ahead_index])
            tokens = tokens[:index] + [{'type': 'NUMBER', 'number': inner_answer}] + tokens[look_ahead_index + 1:]
        index += 1

    # 掛け算と割り算の処理を先にする
    index = 0
    while index < len(tokens):
        

        if tokens[index]['type'] in ['MULTIPLY', 'DIVIDE']:
            if tokens[index]['type'] == 'MULTIPLY':
                tokens[index - 1]['number'] *= tokens[index + 1]['number']
            else:  
                tokens[index - 1]['number'] /= tokens[index + 1]['number']
            # 今のトークンと次のトークンを削除
            del tokens[index:index + 2]
        else:
            index += 1

    # 足し算と引き算の処理
    answer = 0
    tokens.insert(0, {'type': 'PLUS'})  # Insert a dummy '+' token
    index = 1
    while index < len(tokens):
        if tokens[index]['type'] == 'NUMBER':
            if tokens[index - 1]['type'] == 'PLUS':
                answer += tokens[index]['number']
            elif tokens[index - 1]['type'] == 'MINUS':
                answer -= tokens[index]['number']
            else:
                print('Invalid syntax')
                exit(1)
        index += 1
    return answer


def test(line):
    tokens = tokenize(line)
    actual_answer = evaluate(tokens)
    expected_answer = eval(line)
    if abs(actual_answer - expected_answer) < 1e-8:
        print("PASS! (%s = %f)" % (line, expected_answer))
    else:
        print("FAIL! (%s should be %f but was %f)" % (line, expected_answer, actual_answer))


# Add more tests to this function :)
def run_test():
    print("==== Test started! ====")
    test("1+2")
    test("1.0+2.1-3")
    test("5*6")
    test("6/2")
    test("3.0+4*2-1/5")
    test("9-3/2+6*5")
    test("(3.0+4*(2-1))/5")
    test("(5+3)*(2-1)/5")
    print("==== Test finished! ====\n")

run_test()

while True:
    print('> ', end="")
    line = input()
    tokens = tokenize(line)
    answer = evaluate(tokens)
    print("answer = %f\n" % answer)