import tkinter as tk
from enum import Enum
import re
import pandas
import pandastable as pt
from nltk.tree import *


class Token_type(Enum):  # listing all tokens type
    PROGRAM = 1
    END_PROGRAM = 2
    INTEGER = 3
    REAL = 4
    CHARACTER = 5
    IDENTIFIER = 6
    COMPLEX = 7
    TRUE_LOGICAL = 8
    CONSTANT = 9
    IF = 10
    THEN = 11
    ELSE = 12
    END_IF = 13
    DO = 14
    END = 15
    PRINT = 16
    READ = 17

    GREATERTHAN = 18
    SMALLERTHAN = 19
    GREATERTHANOREQUAL = 20
    SMALLERTHANOREQUAL = 21
    EQUALCOMPOP = 22
    NOTEQUALOP = 23
    PLUSOP = 24
    MINUSOP = 25
    MULTIPLICATIONOP = 26
    DIVISIONOP = 27
    COMA = 28
    COLON = 29
    IMPLICITNONE = 30
    SEMI_COLON = 31
    COMMENT_EXCLAMATION = 32
    # BLANK_SPACE=33
    NONE = 34
    OPENPARENTHSIS = 37
    CLOSEPARENTHSIS = 38
    IDENTIFIERERROR = 39
    DOT = 42
    SINGLEQUOTE = 43
    DOUBLEQUOTE = 44
    SIZE = 45
    OPENCURLBRACKET = 46
    CLOSECURLBRACKET = 47
    OPENSQUAREBRACKET = 48
    CLOSESQUAREBRACKET = 49
    FALSE_LOGICAL = 50
    LOGICALOPERATORAND = 51
    LOGICALOPERATOROR = 52
    LOGICALOPERATORNOT = 53
    ELSEIF = 54
    NEWLINE = 55
    STRING = 56
    DOUBLECOLON = 57
    PARAMETER = 58
    BOOLEANTRUE = 59
    LOGICAL = 60
    BOOLEANFALSE = 61
    INTEGERNO = 62
    REALNO = 63
    ENDDO = 64
    ERROR = 65
    EQUAL = 66


# class token to hold string and token type
class token:
    def __init__(self, lex, token_type):
        self.lex = lex
        self.token_type = token_type

    def to_dict(self):
        return {
            'Lex': self.lex,
            'token_type': self.token_type
        }


# Reserved word Dictionary
ReservedWords = {"program": Token_type.PROGRAM,
                 "integer": Token_type.INTEGER,
                 "real": Token_type.REAL,
                 "character": Token_type.CHARACTER,
                 "complex": Token_type.COMPLEX,
                 "and": Token_type.LOGICALOPERATORAND,
                 "or": Token_type.LOGICALOPERATOROR,
                 "not": Token_type.LOGICALOPERATORNOT,
                 "parameter": Token_type.PARAMETER,
                 "if": Token_type.IF,
                 "then": Token_type.THEN,
                 "else": Token_type.ELSE,
                 "elseif": Token_type.ELSEIF,
                 "endif": Token_type.END_IF,
                 "enddo": Token_type.ENDDO,
                 "do": Token_type.DO,
                 "end": Token_type.END,
                 "print*": Token_type.PRINT,
                 "read*": Token_type.READ,
                 "implicitnone": Token_type.IMPLICITNONE,
                 "len": Token_type.SIZE,
                 ".true.": Token_type.TRUE_LOGICAL,
                 "true": Token_type.BOOLEANTRUE,
                 "false": Token_type.BOOLEANFALSE,
                 "logical": Token_type.LOGICAL

                 }
Operators = {">": Token_type.GREATERTHAN,
             "<": Token_type.SMALLERTHAN,
             ">=": Token_type.GREATERTHANOREQUAL,
             "<=": Token_type.SMALLERTHANOREQUAL,
             "==": Token_type.EQUALCOMPOP,
             "=": Token_type.EQUAL,
             "/=": Token_type.NOTEQUALOP,
             "+": Token_type.PLUSOP,
             "-": Token_type.MINUSOP,
             "*": Token_type.MULTIPLICATIONOP,
             "/": Token_type.DIVISIONOP,

             }
Delimiters = {
    # ":": Token_type.COLON,
    "::": Token_type.DOUBLECOLON,
    ";": Token_type.SEMI_COLON,
    ",": Token_type.COMA,

}

Tokens = []  # to add tokens to list
errors = []


def find_token(text):
    neededvariable1 = 0
    arr = []
    text = text.lower()
    delimiters = '\s|,|;|\(|\)|\*|\+|\[|\]|\{|\}|:'

    tokens = re.findall('\w+|\W', text)
    print(tokens)

    i = 0
    while i < len(tokens):
        if (tokens[i] == "!"):
            while (tokens[i] != "\n" or tokens[i] == " "):
                i = i + 1
        elif (tokens[i] == "implicit" and tokens[i + 2] == "none"):
            Tokens.append(token(tokens[i] + " " + tokens[i + 2], Token_type.IMPLICITNONE))
            i = i + 1
            i = i + 2
        elif (tokens[i] == "\n"):
            Tokens.append(token(tokens[i], Token_type.NEWLINE))
            i = i + 1
        elif (tokens[i] == " "):
            i = i + 1
        elif (tokens[i] == "\t"):
            i = i + 1
        elif tokens[i] == "=" and i + 1 < len(tokens) and tokens[i + 1] == "=":
            Tokens.append(token(tokens[i] + tokens[i + 1], Token_type.EQUALCOMPOP))
            i = i + 1
            i = i + 1
        elif tokens[i] == "=" and i + 1 < len(tokens) and tokens[i + 1] != "=":
            Tokens.append(token(tokens[i], Token_type.EQUAL))
            i = i + 1
        elif tokens[i] == ">" and i + 1 < len(tokens) and tokens[i + 1] == "=":
            Tokens.append(token(tokens[i] + tokens[i + 1], Token_type.GREATERTHANOREQUAL))
            i = i + 1
            i = i + 1
        elif tokens[i] == "<" and i + 1 < len(tokens) and tokens[i + 1] == "=":
            Tokens.append(token(tokens[i] + tokens[i + 1], Token_type.SMALLERTHANOREQUAL))
            i = i + 1
            i = i + 1
        elif tokens[i] == "/" and i + 1 < len(tokens) and tokens[i + 1] == "=":
            Tokens.append(token(tokens[i] + tokens[i + 1], Token_type.NOTEQUALOP))
            i = i + 1
            i = i + 1

        elif tokens[i] == "print" and i + 1 < len(tokens) and tokens[i + 1] == "*":
            Tokens.append(token(tokens[i] + tokens[i + 1], Token_type.PRINT))
            i = i + 1
            i = i + 1
        elif tokens[i] == "read" and i + 1 < len(tokens) and tokens[i + 1] == "*":
            Tokens.append(token(tokens[i] + tokens[i + 1], Token_type.READ))
            i = i + 1
            i = i + 1

        elif (tokens[i] == ":" and i + 1 < len(tokens) and tokens[i + 1] == ":"):
            dotvar = tokens[i] + tokens[i + 1]
            Tokens.append(token(dotvar, Token_type.DOUBLECOLON))
            i += 1
            i += 1
        elif tokens[i] == '\n':
            i += 1
        elif tokens[i] == "\"":
            arr.append("")
            i = i + 1
            while tokens[i] != "\"":
                arr[neededvariable1] += tokens[i] + " "
                i = i + 1
                if i < len(tokens) and tokens[i] == "\"":
                    Tokens.append(token("\"", Token_type.DOUBLEQUOTE))
                    Tokens.append(token(arr[neededvariable1], Token_type.STRING))
                    Tokens.append(token("\"", Token_type.DOUBLEQUOTE))
                    arr.append("")
                    i = i + 1
                    neededvariable1 = neededvariable1 + 1
                    break
                elif i == len(tokens) or tokens[i] == "\n":
                    Tokens.append(token("\"", Token_type.DOUBLEQUOTE))
                    Tokens.append(token(arr[neededvariable1], Token_type.ERROR))
                    i = i + 1
                    neededvariable1 = neededvariable1 + 1
                    break

        elif tokens[i] == "\'":
            arr.append("")
            i = i + 1
            while tokens[i] != "\'":
                arr[neededvariable1] += tokens[i] + " "
                i = i + 1
                if i < len(tokens) and tokens[i] == "\'":
                    Tokens.append(token("\'", Token_type.SINGLEQUOTE))
                    Tokens.append(token(arr[neededvariable1], Token_type.STRING))
                    Tokens.append(token("\'", Token_type.SINGLEQUOTE))
                    arr.append("")
                    i = i + 1
                    neededvariable1 = neededvariable1 + 1
                    break
                elif i == len(tokens) or tokens[i] == "\n":
                    Tokens.append(token("\"", Token_type.SINGLEQUOTE))
                    Tokens.append(token(arr[neededvariable1], Token_type.ERROR))
                    break
        elif str(tokens[i]).isdigit() == True and i + 1 < len(tokens) and tokens[i + 1] == "." and i + 2 < len(
                tokens) and str(tokens[i + 2]).isdigit() == True:
            dummyreal = tokens[i] + tokens[i + 1] + tokens[i + 2]
            Tokens.append(token(dummyreal, Token_type.REALNO))
            i = i + 1
            i = i + 1
            i = i + 1
        elif str(tokens[i]).isdigit() == True:
            Tokens.append(token(tokens[i], Token_type.INTEGERNO))
            i = i + 1

        elif tokens[i] == "." and i + 1 < len(tokens) and tokens[i + 1] == "true" and i + 1 < len(tokens) and tokens[
            i + 2] == ".":
            dummytrue = tokens[i] + tokens[i + 1] + tokens[i + 2]
            Tokens.append(token(dummytrue, Token_type.TRUE_LOGICAL))
            i += 1
            i += 1
            i += 1
        elif tokens[i] == "." and i + 1 < len(tokens) and tokens[i + 1] == "true" and i + 2 < len(tokens) and tokens[
            i + 2] != ".":
            dummynottrue = tokens[i] + tokens[i + 1]
            Tokens.append(token(dummynottrue, Token_type.ERROR))
            i += 1
            i += 1
        elif tokens[i] == "." and i + 1 < len(tokens) and tokens[i + 1] == "false" and i + 2 < len(tokens) and tokens[
            i + 2] != ".":
            dummynotfalse = tokens[i] + tokens[i + 1]
            Tokens.append(token(dummynotfalse, Token_type.ERROR))
            i += 1
            i += 1
        elif tokens[i] == "." and i + 1 < len(tokens) and tokens[i + 1] == "false" and i + 2 < len(tokens) and tokens[
            i + 2] == ".":
            dummyfalse = tokens[i] + tokens[i + 1] + tokens[i + 2]
            Tokens.append(token(dummyfalse, Token_type.FALSE_LOGICAL))
            i += 1
            i += 1
            i += 1
        elif tokens[i] in ReservedWords:
            Tokens.append(token(tokens[i], ReservedWords[tokens[i]]))
            i += 1
        elif tokens[i] == "len":
            Tokens.append(token(tokens[i], Token_type.SIZE))
            i += 1
        elif tokens[i] in Operators:
            Tokens.append(token(tokens[i], Operators[tokens[i]]))
            i += 1
        elif tokens[i] in Delimiters:
            Tokens.append(token(tokens[i], Delimiters[tokens[i]]))
            i += 1


        elif tokens[i] == ".":
            Tokens.append(token(tokens[i], Token_type.DOT))
            i += 1
        elif tokens[i] == "\'":
            Tokens.append(token(tokens[i], Token_type.SINGLEQUOTE))
            i += 1
        elif tokens[i] == "\"":
            Tokens.append(token(tokens[i], Token_type.DOUBLEQUOTE))
            i += 1
        elif tokens[i] == "(":
            Tokens.append(token(tokens[i], Token_type.OPENPARENTHSIS))
            i += 1
        elif tokens[i] == ")":
            Tokens.append(token(tokens[i], Token_type.CLOSEPARENTHSIS))
            i += 1
        elif tokens[i] == "{":
            Tokens.append(token(tokens[i], Token_type.OPENCURLBRACKET))
            i += 1
        elif tokens[i] == "}":
            Tokens.append(token(tokens[i], Token_type.CLOSECURLBRACKET))
            i += 1
        elif tokens[i] == "[":
            Tokens.append(token(tokens[i], Token_type.OPENSQUAREBRACKET))
            i += 1
        elif tokens[i] == "]":
            Tokens.append(token(tokens[i], Token_type.CLOSESQUAREBRACKET))
            i += 1
        elif tokens[i] == "!":
            Tokens.append(token(tokens[i], Token_type.COMMENT_EXCLAMATION))
            i += 1

        elif tokens[i] == "true":
            Tokens.append(token(tokens[i], Token_type.TRUE_LOGICAL))
            i += 1
        elif tokens[i] == "false":
            Tokens.append(token(tokens[i], Token_type.FALSE_LOGICAL))
            i += 1
        elif tokens[i] == "and":
            Tokens.append(token(tokens[i], Token_type.LOGICALOPERATORAND))
            i += 1
        elif tokens[i] == "or":
            Tokens.append(token(tokens[i], Token_type.LOGICALOPERATOROR))
            i += 1
        elif tokens[i] == "not":
            Tokens.append(token(tokens[i], Token_type.LOGICALOPERATORNOT))
            i += 1
     

        elif re.match(
                r'[a-z~[idefp]]|[a-z]+[0-9]*|[if][a-z0-9_]+|[do][a-z0-9_]+|[end][a-z0-9_]+|[program][a-z0-9_]+|[integer][a-z0-9_]+',
                tokens[i]):
            Tokens.append(token(tokens[i], Token_type.IDENTIFIER))
            i += 1

          

        else:
            Tokens.append(token(tokens[i], Token_type.ERROR))
            print(Tokens[0].lex)
            i += 1

def Parse():
    j = 0
    Children = []

    Header_dict = Header(j)
    Children.append(Header_dict["node"])

    EndLines_dict = EndLines(Header_dict["index"])
    Children.append(EndLines_dict["node"])

    Declsec_dict = Declsec(EndLines_dict["index"])
    Children.append(Declsec_dict["node"])

    Statements_dict = Statements(Declsec_dict["index"])
    Children.append(Statements_dict["node"])

    End_dict = End(Statements_dict["index"])
    Children.append(End_dict["node"])

    Node = Tree('Program', Children)

    return Node


def EndLines(j):
    out = dict()
    children = []

    o1 = Match(Token_type.NEWLINE, j)
    children.append(o1["node"])

    Elines_dict = Elines(o1["index"])
    children.append(Elines_dict["node"])

    Node = Tree('EndLines', children)
    out["node"] = Node
    out["index"] = Elines_dict["index"]
    return out


def Elines(j):
    out = dict()
    children = []
    Temp = Tokens[j].to_dict()
    if Temp["token_type"] == Token_type.NEWLINE:

        o1 = Match(Token_type.NEWLINE, j)
        children.append(o1["node"])

        Elines_dict = Elines(o1["index"])
        children.append(Elines_dict["node"])

        Node = Tree('Elines', children)
        out["node"] = Node
        out["index"] = Elines_dict["index"]
    else:
        Node = Tree('Elines', children)
        out["node"] = Node
        out["index"] = j
    return out


def Header(j):
    out = dict()
    children = []

    o1 = Match(Token_type.PROGRAM, j)
    children.append(o1["node"])

    o2 = Match(Token_type.IDENTIFIER, o1["index"])
    children.append(o2['node'])

    Node = Tree('Header', children)
    out["node"] = Node
    out["index"] = o2["index"]

    return out


def Declsec(j):
    out = dict()
    children = []
    Temp = Tokens[j].to_dict()

    implicit = Implicit(j)
    if implicit['index'] != j:

        Implicit_dict = implicit
        children.append(Implicit_dict["node"])

        VarDecls_dict = VarDecls(Implicit_dict["index"])
        children.append(VarDecls_dict["node"])

        Node = Tree('Declsec', children)

        out["node"] = Node
        out["index"] = VarDecls_dict["index"]
    else:
        Node = Tree('Declsec', children)
        out["node"] = Node
        out["index"] = j
    return out


def Implicit(j):
    out = dict()
    children = []
    Temp = Tokens[j].to_dict()
    if Temp['token_type'] == Token_type.IMPLICITNONE:

        o1 = Match(Token_type.IMPLICITNONE, j)
        children.append(o1["node"])

        EndLines_dict = EndLines(o1["index"])
        children.append(EndLines_dict["node"])

        Node = Tree('Implicitnone', children)
        out["node"] = Node
        out["index"] = EndLines_dict["index"]
    else:
        Node = Tree('Implicit', children)
        out["node"] = Node
        out["index"] = j

    return out


def VarDecls(j):
    out = dict()
    children = []

    VarDecl_dict = VarDecl(j)
    children.append(VarDecl_dict["node"])

    # EndLines_dict=EndLines(VarDecl_dict["index"])
    # children.append(EndLines_dict["node"])

    VarDeclsDash_dict = VarDeclsDash(VarDecl_dict["index"])
    children.append(VarDeclsDash_dict["node"])

    Node = Tree('VarDecls', children)

    out["node"] = Node
    out["index"] = VarDeclsDash_dict["index"]

    return out


def VarDeclsDash(j):
    out = dict()
    children = []
    VarDecl_dict = VarDecl(j)
    if VarDecl_dict["index"] != j:
        children.append(VarDecl_dict["node"])

        # EndLines_dict=EndLines(VarDecl_dict["index"])
        # children.append(EndLines_dict["node"])

        VarDeclsDash_dict = VarDeclsDash(VarDecl_dict['index'])
        children.append(VarDeclsDash_dict["node"])

        Node = Tree('VarDecl', children)
        out["node"] = Node
        out["index"] = VarDeclsDash_dict["index"]

    else:

        Node = Tree('VarDecl', children)
        out["node"] = Node
        out["index"] = j

    return out


def VarDecl(j):
    out = dict()
    children = []
    Temp = Tokens[j].to_dict()
    DataType_dict = DataType(j)
    if DataType_dict['index'] != j:
        children.append(DataType_dict["node"])

        VarDeclDash_dict = VarDeclDash(DataType_dict["index"])
        children.append(VarDeclDash_dict["node"])

        Node = Tree('VarDecl', children)
        out["node"] = Node
        out["index"] = VarDeclDash_dict["index"]


    else:
        Node = Tree('VarDecl', children)
        out["node"] = Tree('VarDecl', children)
        out["index"] = j
    return out


def VarDeclDash(j):
    out = dict()
    children = []
    Temp = Tokens[j].to_dict()
    if (Temp['token_type'] == Token_type.DOUBLECOLON):

        o1 = Match(Token_type.DOUBLECOLON, j)
        children.append(o1["node"])

        Idlist_dict = Idlist(o1["index"])
        children.append(Idlist_dict["node"])

        VarDeclDoubleDash_dict = VarDeclDoubleDash(Idlist_dict["index"])
        children.append(VarDeclDoubleDash_dict["node"])

        EndLines_dict = EndLines(VarDeclDoubleDash_dict["index"])
        children.append(EndLines_dict["node"])

        Node = Tree('VarDeclDash', children)
        out["node"] = Node
        out["index"] = EndLines_dict["index"]
    else:
        o1 = Match(Token_type.COMA, j)
        children.append(o1["node"])

        o2 = Match(Token_type.PARAMETER, o1["index"])
        children.append(o2["node"])

        o3 = Match(Token_type.DOUBLECOLON, o2["index"])
        children.append(o3["node"])

        Idlist_dict = Idlist(o3["index"])
        children.append(Idlist_dict["node"])

        o4 = Match(Token_type.EQUAL, Idlist_dict["index"])
        children.append(o4["node"])

        Number_dict = Number(o4["index"])
        children.append(Number_dict["node"])

        EndLines_dict = EndLines(Number_dict["index"])
        children.append(EndLines_dict["node"])

        Node = Tree('VarDeclDash', children)
        out["node"] = Node
        out["index"] = EndLines_dict["index"]

    return out


def Number(j):
    out = dict()
    children = []
    Temp = Tokens[j].to_dict()
    if Temp['token_type'] == Token_type.INTEGERNO:
        o1 = Match(Token_type.INTEGERNO, j)
        children.append(o1["node"])
    else:
        o1 = Match(Token_type.REALNO, j)
        children.append(o1["node"])
    Node = Tree('Number', children)
    out["node"] = Node
    out["index"] = o1["index"]
    return out


def VarDeclDoubleDash(j):
    out = dict()
    children = []
    Temp = Tokens[j].to_dict()
    if (Temp['token_type'] == Token_type.EQUAL):
        o1 = Match(Token_type.EQUAL, j)
        children.append(o1["node"])

        # Expression_dict = Expression(o1["index"])
        # children.append(Expression_dict["node"])
        AssignmentDash_dict = AssignmentDash(o1["index"])
        children.append(AssignmentDash_dict["node"])

        MoreDecl_dict = MoreDecl(AssignmentDash_dict["index"])
        children.append(MoreDecl_dict["node"])

        # EndLines_dict = EndLines(MoreDecl_dict["index"])
        # children.append(EndLines_dict["node"])

        Node = Tree('VarDeclDoubleDash', children)
        out["node"] = Node
        out["index"] = MoreDecl_dict["index"]

    else:
        Node = Tree('VarDeclDoubleDash', children)
        out["node"] = Node
        out["index"] = j
    return out


def MoreDecl(j):
    out = dict()
    children = []
    Temp = Tokens[j].to_dict()
    if (Temp['token_type'] == Token_type.COMA):
        o1 = Match(Token_type.COMA, j)
        children.append(o1["node"])

        o2 = Match(Token_type.IDENTIFIER, o1["index"])
        children.append(o2["node"])

        o3 = Match(Token_type.EQUAL, o2["index"])
        children.append(o3["node"])

        Expression_dict = Expression(o3["index"])
        children.append(Expression_dict["node"])

        MoreDecl_dict = MoreDecl(Expression_dict["index"])
        children.append(MoreDecl_dict["node"])

        Node = Tree('MoreDecl', children)
        out["node"] = Node
        out["index"] = MoreDecl_dict["index"]
    else:
        Node = Tree('MoreDecl', children)
        out["node"] = Node
        out["index"] = j
    return out


def Bool(j):
    out = dict()
    children = []
    Temp = Tokens[j].to_dict()

    if (Temp['token_type'] == Token_type.TRUE_LOGICAL):
        o1 = Match(Token_type.TRUE_LOGICAL, j)
        children.append(o1["node"])

    else:
        o1 = Match(Token_type.FALSE_LOGICAL, j)
        children.append(o1["node"])

    Node = Tree('Bool', children)
    out["node"] = Node
    out["index"] = o1["index"]
    return out


def DataType(j):
    out = dict()
    children = []
    flag = False
    Temp = Tokens[j].to_dict()

    if (Temp['token_type'] == Token_type.INTEGER):
        o1 = Match(Token_type.INTEGER, j)
        children.append(o1["node"])


    elif (Temp['token_type'] == Token_type.REAL):
        o1 = Match(Token_type.REAL, j)
        children.append(o1["node"])

    elif (Temp['token_type'] == Token_type.COMPLEX):
        o1 = Match(Token_type.COMPLEX, j)
        children.append(o1["node"])

    elif (Temp['token_type'] == Token_type.LOGICAL):
        o1 = Match(Token_type.LOGICAL, j)
        children.append(o1["node"])

    elif (Temp['token_type'] == Token_type.CHARACTER):
        Character_dict = Character(j)
        children.append(Character_dict["node"])
        flag = True
    else:
        Node = Tree('DataType', children)
        out["node"] = Node
        out["index"] = j
        return out

    Node = Tree('DataType', children)
    out["node"] = Node
    if not flag:
        out["index"] = o1["index"]
    else:
        out["index"] = Character_dict["index"]
    return out


def Character(j):
    out = dict()
    children = []

    o1 = Match(Token_type.CHARACTER, j)
    children.append(o1["node"])

    CharacterDash_dict = CharacterDash(o1["index"])
    children.append(CharacterDash_dict["node"])

    Node = Tree('Character', children)
    out["node"] = Node
    out["index"] = CharacterDash_dict["index"]
    return out


def CharacterDash(j):
    out = dict()
    children = []
    Temp = Tokens[j].to_dict()
    if (Temp['token_type'] == Token_type.OPENPARENTHSIS):
        o1 = Match(Token_type.OPENPARENTHSIS, j)
        children.append(o1["node"])

        o2 = Match(Token_type.SIZE, o1["index"])

        children.append(o2["node"])

        o3 = Match(Token_type.EQUAL, o2["index"])
        children.append(o3["node"])

        o4 = Match(Token_type.INTEGERNO, o3["index"])
        children.append(o4["node"])

        o5 = Match(Token_type.CLOSEPARENTHSIS, o4["index"])
        children.append(o5["node"])
        Node = Tree('CharacterDash', children)
        out["node"] = Node
        out["index"] = o5["index"]
    else:
        Node = Tree('CharacterDash', children)
        out["node"] = Node
        out["index"] = j

    return out


def Idlist(j):
    out = dict()
    children = []

    o1 = Match(Token_type.IDENTIFIER, j)
    children.append(o1["node"])

    IdListDash_dict = IdlistDash(o1['index'])
    children.append(IdListDash_dict["node"])

    Node = Tree('Idlist', children)

    out["node"] = Node
    out["index"] = IdListDash_dict["index"]
    return out


def IdlistDash(j):
    out = dict()
    children = []
    Temp = Tokens[j].to_dict()
    if (Temp['token_type'] == Token_type.COMA):
        o1 = Match(Token_type.COMA, j)
        children.append(o1["node"])

        o2 = Match(Token_type.IDENTIFIER, o1['index'])
        children.append(o2["node"])

        IdListDash_dict = IdlistDash(o2['index'])
        children.append(IdListDash_dict["node"])

        Node = Tree('Idlist', children)

        out["node"] = Node
        out["index"] = IdListDash_dict["index"]
    else:
        Node = Tree('IdlistDash', children)
        out["node"] = Node
        out["index"] = j
    return out


def Statements(j):
    out = dict()
    children = []

    Statement_dict = Statement(j)
    children.append(Statement_dict["node"])

    # EndLines_dict = EndLines(Statement_dict['index'])
    # children.append(EndLines_dict["node"])

    StatementsDash_dict = StatementsDash(Statement_dict['index'])
    children.append(StatementsDash_dict["node"])

    Node = Tree('Statements', children)
    out["node"] = Node
    out["index"] = StatementsDash_dict["index"]

    return out


def StatementsDash(j):
    out = dict()
    children = []
    Statement_dict = Statement(j)
    if Statement_dict["index"] != j:
        children.append(Statement_dict["node"])

        # EndLines_dict = EndLines(Statement_dict['index'])
        # children.append(EndLines_dict["node"])

        StatementsDash_dict = StatementsDash(Statement_dict['index'])
        children.append(StatementsDash_dict["node"])

        Node = Tree('StatementsDash', children)
        out["node"] = Node
        out["index"] = StatementsDash_dict["index"]
    else:
        Node = Tree('StatementsDash', [])
        out["node"] = Node
        out["index"] = j

    return out


def Statement(j):
    out = dict()
    children = []

    Temp = Tokens[j].to_dict()
    if Temp['token_type'] == Token_type.READ:
        o1 = Match(Token_type.READ, j)
        children.append(o1["node"])

        o2 = Match(Token_type.COMA, o1['index'])
        children.append(o2["node"])

        IdList_dict = Idlist(o2['index'])
        children.append(IdList_dict["node"])

        EndLines_dict = EndLines(IdList_dict['index'])
        children.append(EndLines_dict["node"])

        Node = Tree('Statement', children)
        out["node"] = Node
        out["index"] = EndLines_dict["index"]


    elif (Temp['token_type'] == Token_type.PRINT):

        Print_dict = Printt(j)
        children.append(Print_dict["node"])

        EndLines_dict = EndLines(Print_dict['index'])
        children.append(EndLines_dict["node"])

        Node = Tree('Statement', children)
        out["node"] = Node
        out["index"] = EndLines_dict["index"]


    elif (Temp['token_type'] == Token_type.IF):
        If_dict = If(j)
        children.append(If_dict["node"])

        EndLines_dict = EndLines(If_dict['index'])
        children.append(EndLines_dict["node"])

        Node = Tree('Statement', children)
        out["node"] = Node
        out["index"] = EndLines_dict["index"]

    elif (Temp['Lex'] == "do"):

        o1 = Match(Token_type.DO, j)
        children.append(o1["node"])

        DoParams_dict = DoParams(o1['index'])
        children.append(DoParams_dict["node"])

        EndLines_dict = EndLines(DoParams_dict['index'])
        children.append(EndLines_dict["node"])

        Statements_dict = Statements(EndLines_dict['index'])
        children.append(Statements_dict["node"])

        o4 = Match(Token_type.ENDDO, Statements_dict['index'])
        children.append(o4["node"])

        EndLines_dict = EndLines(o4['index'])
        children.append(EndLines_dict["node"])

        Node = Tree('Statement', children)
        out["node"] = Node
        out["index"] = EndLines_dict["index"]

    elif (Temp['token_type'] == Token_type.IDENTIFIER):
        Assignment_dict = Assignment(j)
        children.append(Assignment_dict["node"])

        EndLines_dict = EndLines(Assignment_dict['index'])
        children.append(EndLines_dict["node"])

        Node = Tree('Statement', children)
        out["node"] = Node
        out["index"] = EndLines_dict["index"]

    else:
        Node = Tree('Statement', children)
        out["node"] = Node
        out["index"] = j
    return out


def DoParams(j):
    out = dict()
    children = []
    Temp = Tokens[j].to_dict()
    if Temp['token_type'] == Token_type.IDENTIFIER:
        o1 = Match(Token_type.IDENTIFIER, j)
        children.append(o1["node"])

        o2 = Match(Token_type.EQUAL, o1['index'])
        children.append(o2["node"])

        DoIdentifierList_dict = DoIdentifierList(o2['index'])
        children.append(DoIdentifierList_dict["node"])

        Node = Tree('DoParams', children)
        out["node"] = Node
        out["index"] = DoIdentifierList_dict["index"]
    else:
        Node = Tree('DoParams', children)
        out["node"] = Node
        out["index"] = j
    return out


def Assignment(j):
    out = dict()
    children = []
    Temp = Tokens[j].to_dict()
    o1 = Match(Token_type.IDENTIFIER, j)
    children.append(o1["node"])

    o2 = Match(Token_type.EQUAL, o1['index'])
    children.append(o2["node"])

    AssignmentDash_dict = AssignmentDash(o2['index'])
    children.append(AssignmentDash_dict["node"])

    Node = Tree('Assignment', children)
    out["node"] = Node
    out["index"] = AssignmentDash_dict["index"]
    return out


def AssignmentDash(j):
    out = dict()
    children = []
    Temp = Tokens[j].to_dict()
    if Temp['token_type'] == Token_type.TRUE_LOGICAL or Temp['token_type'] == Token_type.FALSE_LOGICAL:
        Bool_dict = Bool(j)
        children.append(Bool_dict["node"])

        Node = Tree('AssignmentDash', children)
        out["node"] = Node
        out["index"] = Bool_dict["index"]
    elif Temp['token_type'] == Token_type.DOUBLEQUOTE:
        o1 = Match(Token_type.DOUBLEQUOTE, j)
        children.append(o1["node"])

        o2 = Match(Token_type.STRING, o1['index'])
        children.append(o2["node"])

        o3 = Match(Token_type.DOUBLEQUOTE, o2['index'])
        children.append(o3["node"])

        Node = Tree('AssignmentDash', children)
        out["node"] = Node
        out["index"] = o3["index"]
    elif Temp['token_type'] == Token_type.SINGLEQUOTE:
        o1 = Match(Token_type.SINGLEQUOTE, j)
        children.append(o1["node"])

        o2 = Match(Token_type.STRING, o1['index'])
        children.append(o2["node"])

        o3 = Match(Token_type.SINGLEQUOTE, o2['index'])
        children.append(o3["node"])

        Node = Tree('AssignmentDash', children)
        out["node"] = Node
        out["index"] = o3["index"]
    else:
        Expression_dict = Expression(j)
        children.append(Expression_dict["node"])

        Node = Tree('AssignmentDash', children)
        out["node"] = Node
        out["index"] = Expression_dict["index"]
    return out


def Printt(j):
    out = dict()
    children = []
    o1 = Match(Token_type.PRINT, j)
    children.append(o1["node"])

    PrintDash_dict = PrintDash(o1['index'])
    children.append(PrintDash_dict["node"])

    Node = Tree('Print', children)
    out["node"] = Node
    out["index"] = PrintDash_dict["index"]
    return out


def PrintDash(j):
    out = dict()
    children = []
    Prints_dict = Prints(j)
    if Prints_dict["index"] != j:

        children.append(Prints_dict["node"])

        Node = Tree('PrintDash', children)
        out["node"] = Node
        out["index"] = Prints_dict["index"]
    else:
        Expression_dict = Expression(j)
        children.append(Expression_dict["node"])

        Node = Tree('PrintDash', children)
        out["node"] = Node
        out["index"] = Expression_dict["index"]

    return out


def Prints(j):
    out = dict()
    children = []
    PrintDecl_dict = PrintDecl(j)
    children.append(PrintDecl_dict["node"])

    PrintsDash_dict = PrintsDash(PrintDecl_dict['index'])
    children.append(PrintsDash_dict["node"])

    Node = Tree('Prints', children)
    out["node"] = Node
    out["index"] = PrintsDash_dict["index"]
    return out


def PrintsDash(j):
    out = dict()
    children = []
    PrintDecl_dict = PrintDecl(j)
    if PrintDecl_dict["index"] != j:

        children.append(PrintDecl_dict["node"])

        PrintsDash_dict = PrintsDash(PrintDecl_dict['index'])
        children.append(PrintsDash_dict["node"])

        Node = Tree('PrintsDash', children)
        out["node"] = Node
        out["index"] = PrintsDash_dict["index"]
    else:
        Node = Tree('PrintsDash', children)
        out["node"] = Node
        out["index"] = j
    return out


def PrintDecl(j):
    out = dict()
    children = []

    if Tokens[j].to_dict()['token_type'] == Token_type.COMA:
        o1 = Match(Token_type.COMA, j)
        children.append(o1["node"])

        PrintList_dict = PrintList(o1['index'])
        children.append(PrintList_dict["node"])

        Node = Tree('PrintDecl', children)
        out["node"] = Node
        out["index"] = PrintList_dict["index"]
    else:
        Node = Tree('PrintDecl', children)
        out["node"] = Node
        out["index"] = j
    return out


def PrintList(j):
    out = dict()
    children = []
    if Tokens[j].to_dict()['token_type'] == Token_type.DOUBLEQUOTE:
        o1 = Match(Token_type.DOUBLEQUOTE, j)
        children.append(o1["node"])

        o2 = Match(Token_type.STRING, o1['index'])
        children.append(o2["node"])

        o3 = Match(Token_type.DOUBLEQUOTE, o2['index'])
        children.append(o3["node"])

        Node = Tree('PrintList', children)
        out["node"] = Node
        out["index"] = o3["index"]

    elif Tokens[j].to_dict()['token_type'] == Token_type.SINGLEQUOTE:
        o1 = Match(Token_type.SINGLEQUOTE, j)
        children.append(o1["node"])

        o2 = Match(Token_type.STRING, o1['index'])
        children.append(o2["node"])

        o3 = Match(Token_type.SINGLEQUOTE, o2['index'])
        children.append(o3["node"])

        Node = Tree('PrintList', children)
        out["node"] = Node
        out["index"] = o3["index"]

    else:
        o1 = Match(Token_type.IDENTIFIER, j)
        children.append(o1["node"])

        Node = Tree('PrintList', children)
        out["node"] = Node
        out["index"] = o1["index"]
    return out


def DoIdentifierList(j):
    out = dict()
    children = []

    DoBoundaries_dict = DoBoundaries(j)
    children.append(DoBoundaries_dict["node"])

    o2 = Match(Token_type.COMA, DoBoundaries_dict['index'])
    children.append(o2["node"])

    DoBoundaries_dict2 = DoBoundaries(o2['index'])
    children.append(DoBoundaries_dict2["node"])

    DoIdentifierListDash_dict = DoIdentifierListDash(DoBoundaries_dict2['index'])
    children.append(DoIdentifierListDash_dict["node"])

    Node = Tree('DoIdentifierList', children)
    out["node"] = Node
    out["index"] = DoIdentifierListDash_dict["index"]

    return out


def DoBoundaries(j):
    out = dict()
    children = []
    Temp = Tokens[j].to_dict()
    if Temp['token_type'] == Token_type.IDENTIFIER:
        o1 = Match(Token_type.IDENTIFIER, j)
        children.append(o1["node"])
    else:
        o1 = Match(Token_type.INTEGERNO, j)
        children.append(o1["node"])
    Node = Tree('DoBoundaries', children)
    out["node"] = Node
    out["index"] = o1["index"]
    return out


def DoIdentifierListDash(j):
    out = dict()
    children = []

    if Tokens[j].to_dict()['token_type'] == Token_type.COMA:
        o1 = Match(Token_type.COMA, j)
        children.append(o1["node"])

        Factor_dict = Factor(o1['index'])
        children.append(Factor_dict["node"])

        Node = Tree('DoIdentifierListDash', children)
        out["node"] = Node
        out["index"] = Factor_dict["index"]
    else:
        Node = Tree('DoIdentifierListDash', children)
        out["node"] = Node
        out["index"] = j

    return out


#######################   Zeina  #########################

def If(j):
    out = dict()
    children = []
    o1 = Match(Token_type.IF, j)
    children.append(o1["node"])

    Condition_dict = Condition(o1["index"])
    children.append(Condition_dict["node"])

    o2 = Match(Token_type.THEN, Condition_dict["index"])
    children.append(o2["node"])

    EndLines_dict = EndLines(o2["index"])
    children.append(EndLines_dict["node"])

    Statements_dict = Statements(EndLines_dict["index"])
    children.append(Statements_dict["node"])

    # EndLines_dict2=EndLines(Statements_dict["index"])
    # children.append(EndLines_dict2["node"])

    Else_dict = Else(Statements_dict["index"])
    children.append(Else_dict["node"])

    o3 = Match(Token_type.END_IF, Else_dict["index"])
    children.append(o3["node"])

    Node = Tree('If', children)
    out["node"] = Node
    out["index"] = o3["index"]
    return out


def Else(j):
    out = dict()
    children = []
    Temp = Tokens[j].to_dict()
    if Temp['token_type'] == Token_type.ELSEIF:

        Elseif_dict = Elseif(j)
        children.append(Elseif_dict["node"])

        Node = Tree('Else', children)
        out["node"] = Node
        out["index"] = Elseif_dict["index"]

    elif Temp['token_type'] == Token_type.ELSE:
        o1 = Match(Token_type.ELSE, j)
        children.append(o1["node"])

        EndLines_dict = EndLines(o1["index"])
        children.append(EndLines_dict["node"])

        Statements_dict = Statements(EndLines_dict["index"])
        children.append(Statements_dict["node"])

        Node = Tree('Else', children)
        out["node"] = Node
        out["index"] = Statements_dict["index"]
    else:

        Node = Tree('Else', children)
        out["node"] = Node
        out["index"] = j
    return out


def Elseif(j):
    out = dict()
    children = []
    Temp = Tokens[j].to_dict()
    if Temp['token_type'] == Token_type.ELSEIF:
        o1 = Match(Token_type.ELSEIF, j)
        children.append(o1["node"])

        Condition_dict = Condition(o1["index"])
        children.append(Condition_dict["node"])

        o2 = Match(Token_type.THEN, Condition_dict["index"])
        children.append(o2["node"])

        EndLines_dict = EndLines(o2["index"])
        children.append(EndLines_dict["node"])

        Statements_dict = Statements(EndLines_dict["index"])
        children.append(Statements_dict["node"])

        Else_dict = Else(Statements_dict["index"])
        children.append(Else_dict["node"])

        Node = Tree('Elseif', children)
        out["node"] = Node
        out["index"] = Else_dict["index"]
    else:
        Node = Tree('Elseif', children)
        out["node"] = Node
        out["index"] = j
    return out


def Condition(j):
    out = dict()
    children = []

    o1 = Match(Token_type.OPENPARENTHSIS, j)
    children.append(o1["node"])
    Expression_dict = Expression(o1["index"])
    children.append(Expression_dict["node"])

    RelOp_dict = RelOp(Expression_dict["index"])
    children.append(RelOp_dict["node"])

    Expression_dict = Expression(RelOp_dict["index"])
    children.append(Expression_dict["node"])

    o2 = Match(Token_type.CLOSEPARENTHSIS, Expression_dict["index"])
    children.append(o2["node"])

    Node = Tree('Condition', children)
    out["node"] = Node
    out["index"] = o2["index"]

    return out


def Expression(j):
    out = dict()
    children = []

    Term_dict = Term(j)

    children.append(Term_dict["node"])
    ExpressionDash_dict = ExpressionDash(Term_dict["index"])
    children.append(ExpressionDash_dict["node"])

    Node = Tree('Expression', children)
    out["node"] = Node
    out["index"] = ExpressionDash_dict["index"]

    return out


def ExpressionDash(j):
    out = dict()
    children = []
    Temp = Tokens[j].to_dict()
    if Temp['token_type'] == Token_type.PLUSOP or Temp['token_type'] == Token_type.MINUSOP:
        AddOp_dict = AddOp(j)
        children.append(AddOp_dict["node"])

        Term_dict = Term(AddOp_dict["index"])
        children.append(Term_dict["node"])

        ExpressionDash_dict = ExpressionDash(Term_dict["index"])
        children.append(ExpressionDash_dict["node"])

        Node = Tree('ExpressionDash', children)
        out["node"] = Node
        out["index"] = ExpressionDash_dict["index"]
    else:
        Node = Tree('ExpressionDash', children)
        out["node"] = Node
        out["index"] = j
    return out


def Term(j):
    out = dict()
    children = []

    Factor_dict = Factor(j)
    children.append(Factor_dict["node"])

    TermDash_dict = TermDash(Factor_dict["index"])
    children.append(TermDash_dict["node"])

    Node = Tree('Term', children)
    out["node"] = Node
    out["index"] = TermDash_dict["index"]
    return out


def TermDash(j):
    out = dict()
    children = []

    Temp = Tokens[j].to_dict()
    if Temp['token_type'] == Token_type.MULTIPLICATIONOP or Temp['token_type'] == Token_type.DIVISIONOP:
        MultOp_dict = MultOp(j)
        children.append(MultOp_dict["node"])

        Factor_dict = Factor(MultOp_dict["index"])
        children.append(Factor_dict["node"])

        TermDash_dict = TermDash(Factor_dict["index"])
        children.append(TermDash_dict["node"])

        Node = Tree('TermDash', children)
        out["node"] = Node
        out["index"] = TermDash_dict["index"]
    else:
        Node = Tree('TermDash', children)
        out["node"] = Node
        out["index"] = j
    return out


def Factor(j):
    out = dict()
    children = []
    Temp = Tokens[j].to_dict()
    if Temp['token_type'] == Token_type.IDENTIFIER:
        o1 = Match(Token_type.IDENTIFIER, j)
        children.append(o1["node"])
        Node = Tree('Factor', children)
        out["node"] = Node
        out["index"] = o1["index"]
    elif Temp['token_type'] == Token_type.OPENPARENTHSIS:
        o1 = Match(Token_type.OPENPARENTHSIS, j)
        children.append(o1["node"])

        Expression_dict = Expression(o1["index"])
        children.append(Expression_dict["node"])
        o2 = Match(Token_type.CLOSEPARENTHSIS, Expression_dict["index"])
        children.append(o2["node"])
        Node = Tree('Factor', children)
        out["node"] = Node
        out["index"] = o2["index"]

    else:
        Number_dict = Number(j)
        children.append(Number_dict["node"])
        Node = Tree('Factor', children)
        out["node"] = Node
        out["index"] = Number_dict["index"]

    return out


def AddOp(j):
    out = dict()
    children = []
    Temp = Tokens[j].to_dict()
    if Temp['token_type'] == Token_type.PLUSOP:
        o1 = Match(Token_type.PLUSOP, j)

    else:
        o1 = Match(Token_type.MINUSOP, j)

    children.append(o1["node"])
    Node = Tree('AddOp', children)
    out["node"] = Node
    out["index"] = o1["index"]

    return out


def MultOp(j):
    out = dict()
    children = []
    Temp = Tokens[j].to_dict()
    if Temp['token_type'] == Token_type.MULTIPLICATIONOP:
        o1 = Match(Token_type.MULTIPLICATIONOP, j)

    else:
        o1 = Match(Token_type.DIVISIONOP, j)

    children.append(o1["node"])
    Node = Tree('MultOp', children)
    out["node"] = Node
    out["index"] = o1["index"]
    return out


def RelOp(j):
    out = dict()
    children = []

    Temp = Tokens[j].to_dict()
    if Temp['token_type'] == Token_type.GREATERTHANOREQUAL:
        o1 = Match(Token_type.GREATERTHANOREQUAL, j)

    elif Temp['token_type'] == Token_type.GREATERTHAN:
        o1 = Match(Token_type.GREATERTHAN, j)


    elif Temp['token_type'] == Token_type.SMALLERTHANOREQUAL:
        o1 = Match(Token_type.SMALLERTHANOREQUAL, j)

    elif Temp['token_type'] == Token_type.SMALLERTHAN:
        o1 = Match(Token_type.SMALLERTHAN, j)

    elif Temp['token_type'] == Token_type.EQUALCOMPOP:
        o1 = Match(Token_type.EQUALCOMPOP, j)

    else:
        o1 = Match(Token_type.NOTEQUALOP, j)

    children.append(o1["node"])
    Node = Tree('RelOp', children)
    out["node"] = Node
    out["index"] = o1["index"]
    return out


def End(j):
    out = dict()
    children = []

    o1 = Match(Token_type.END, j)
    children.append(o1['node'])

    o2 = Match(Token_type.PROGRAM, o1['index'])
    children.append(o2['node'])

    o3 = Match(Token_type.IDENTIFIER, o2['index'])
    children.append(o3['node'])

    Node = Tree('End', children)
    out["node"] = Node
    out["index"] = o3["index"]

    return out


def Match(a, j):
    # a -> el token el ana badawar 3aleha
    output = dict()
    if (j < len(Tokens)):
        Temp = Tokens[j].to_dict()
        if (Temp['token_type'] == a):
            j += 1
            output["node"] = [Temp['Lex']]
            output["index"] = j
            # print("Matched "+Temp['Lex'])
            return output
        else:
            output["node"] = ["error"]
            output["index"] = j
            errors.append("Syntax error : " + Temp['Lex'] + " Expected " + str(a))
            print("Syntax error : " + Temp['Lex'] + " Expected " + str(a))
            return output
    else:
        output["node"] = ["error"]
        output["index"] = j
        return output







root = tk.Tk()
canvas1 = tk.Canvas(root, width=400, height=50, relief='raised')
canvas1.pack()


# Create a list of image URLs or file paths








canvas1 = tk.Canvas(root, width=400, height=300, relief='raised')
canvas1.pack()

label1 = tk.Label(root, text='Fortran Compiler')
label1.config(font=('helvetica', 14))
canvas1.create_window(200, 25, window=label1)

label2 = tk.Label(root, text='Source code:')
label2.config(font=('helvetica', 10))
canvas1.create_window(200, 100, window=label2)

entry1 = tk.Text(root, height=10, width=50)

canvas1.create_window(200, 140, window=entry1)


word_list = []






def Scan_scanner():
    x1 = entry1.get("1.0", tk.END)
    find_token(x1)
    df = pandas.DataFrame.from_records([t.to_dict() for t in Tokens])
    # to display token stream as table
    dTDa1 = tk.Toplevel()
    dTDa1.title('Token Stream')
    if x1:  # Check if the input is not empty
        word_list.append(x1)
        frame = tk.Frame(root)
        frame.pack()


        canvas1 = tk.Canvas(root, width=400, height=300, relief='raised')
        canvas1.pack()


    dTDaPT = pt.Table(dTDa1, dataframe=df, showtoolbar=True, showstatusbar=True)
    dTDaPT.show()



def Scan_parser():
    x1 = entry1.get("1.0", tk.END)
    find_token(x1)
    df = pandas.DataFrame.from_records([t.to_dict() for t in Tokens])
    # start Parsing
    Node = Parse()
    df1 = pandas.DataFrame(errors)
    dTDa2 = tk.Toplevel()
    dTDa2.title('Error List')
    dTDaPT2 = pt.Table(dTDa2, dataframe=df1, showtoolbar=True, showstatusbar=True)
    dTDaPT2.show()
    Node.draw()


button1 = tk.Button(text='Scan', command=Scan_scanner, bg='blue', fg='white', font=('helvetica', 9, 'bold'))
canvas1.create_window(150, 250,width=100, height=50, window=button1)

button2 = tk.Button(text='Parse', command=Scan_parser, bg='red', fg='white', font=('helvetica', 9, 'bold'))
canvas1.create_window(250, 250,width=100, height=50, window=button2)

root = tk.Tk()
canvas1 = tk.Canvas(root, width=400, height=300, relief='raised')
canvas1.pack()
root.mainloop()


