import sublime_plugin

class IncrementSelectionCommand(sublime_plugin.TextCommand):
    digits = '0123456789'
    letters = 'abcdefghijklmnopqrstuvwxyz'
    special = '#'

    def run(self, edit):
        arr = self.view.substr(self.view.sel()[0]).replace(' ', '').split(',')
        second_digit = self.view.substr(self.view.sel()[1]).replace(' ', '').split(',')
        start = arr[0]
        if len(arr) == 1:

            diff = 0
            if start == '':
                step = 1
            elif start[0] in self.digits:
                diff = int(second_digit[0]) - int(start)
            elif start[0].lower() in self.letters:
                diff = self.letterDecode(second_digit[0].lower()) - self.letterDecode(start[0].lower())

            if diff != 0:
                step = diff
            else:
                step = 1
        else:
            step = int(arr[1])

        if start == '':
            start = 1
            def gen(counter):
                return str(start + counter)

        elif start[0] in self.digits:
            if start[0] == '0':
                length = len(start)
                start = int(start)
                def gen(counter):
                    result = str(start + counter)
                    while len(result) < length:
                        result = '0' + result
                    return result
            else:
                start = int(start)
                def gen(counter):
                    return str(start + counter)

        elif start[0] in self.letters:
            start = self.letterDecode(start)
            def gen(counter):
                print((start+counter-1)%26+1)
                return self.letterEncode((start + counter-1)%26+1)

        elif start[0] in self.letters.upper():
            start = self.letterDecode(start.lower())
            def gen(counter):
                return self.letterEncode((start + counter-1)%26+1).upper()

        elif start[0] in self.special:
            if start[0] == '#':
                def gen(counter):
                    return str(self.view.rowcol(selection.begin())[0] + 1)

        else :
            return

        counter = 0

        for selection in self.view.sel():
            self.view.insert(edit, selection.begin(), gen(counter))
            counter += step

        for selection in self.view.sel():
            self.view.erase(edit, selection)

    def letterEncode(self, number):
        result = ''

        while number > 0:
            number -= 1
            result = self.letters[number % 26] + result
            number //= 26

        return result

    def letterDecode(self, str):
        result = 0

        for i in str:
            result *= 26
            result += self.letters.index(i) + 1

        return result
