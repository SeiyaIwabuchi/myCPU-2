"""
命令はnote.mdを参照
"""
import sys

mnemonicTable = {
    "LDM":"2",
    "LDR":"3",
    "ST":"4",
    "JZE":"5",
    "JMI":"6",
    "NOP":"0",
    "ADD":"1",
    }
labelTable = {}
if len(sys.argv) < 3:
    print("引数不足")
    quit()

sc = open(sys.argv[1],"r").read() #ソースファイル
of = open(sys.argv[2],"w") #バイナリファイル
binStr = ""
address = 0
mnemonics = list(mnemonicTable.keys())
for sent in sc.split("\n"):
    sent = sent.split()
    if sent[0] in [mnemonics[0],mnemonics[2]]:
        binStr += mnemonicTable[sent[0]] + " "
        binStr += str(int(sent[1],16)+1) + " "
        try:
            binStr += str(int(sent[2],16)) + " "
        except ValueError:
            try:
                binStr += labelTable[sent[2]] + " "
            except KeyError:
                print("ラベル名が見つかりません。")
                print(sent[2])
                quit()
        address += 3
    elif sent[0] in [mnemonics[1],mnemonics[6]]:
        binStr += mnemonicTable[sent[0]] + " "
        binStr += str(int(sent[1])+1) + " "
        binStr += sent[2] + " "
        address += 3
    elif sent[0] in [mnemonics[3],mnemonics[4]]:
        binStr += mnemonicTable[sent[0]] + " "
        binStr += "0 "
        binStr += sent[1] + " "
        address += 3
    elif sent[0] == mnemonics[5]:
        binStr += "0 0 0 "
        address += 3
    elif sent[0] == "DC":
        binStr += sent[1]
        address += 1
    elif sent[0] == "DS":
        for i in range(int(sent[1],16)):
            binStr += "0 "
            address += 1
    else:
        label = sent[0]
        if not sent[1] in ["DC","DS"]:
            print("文法エラー")
            print(sent)
            quit()
        try:
            sent[2]
        except IndexError:
            print("文法エラー")
            print(sent)
            quit()
        if sent[1] == "DC":
            binStr += sent[2] + " "
            labelTable[label] = str(address)
            address += 1
        elif sent[1] == "DS":
            labelTable[label] = str(address)
            for i in range(int(sent[2],16)):
                binStr += "0 "
                address += 1
print(binStr)
binStr = binStr.split()
outStr = "v2.0 raw\n"
c = 0
for c,b in enumerate(binStr):
    outStr += b + " "
    if (c+1)%8 == 0:
        outStr += "\n"
for i in range(8-((c+1)%8)):
    outStr += "0 "
print(outStr)
of.write(outStr)