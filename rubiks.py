#Dahlia Dry
#4.18.2019
#Rubiks Cube Blindsolve Practice Tool
import pandas as pd
import numpy as np
from vpython import *
from math import pi,sin,cos
import random

class Rubiks(object):
    """*****Rubiks Cube Blindsolve Practice Tool
    Parameters
    ----------
    solvedconfig: pandas df of cubit positions and orientations in solved configuration
    cubits: pandas df of current cubit positions and orientations"""
    def __init__(self):
        self.solvedconfig = pd.read_csv("solvedconfig.txt", sep=" ")
        for i in range(len(self.solvedconfig)):
            ppos = self.solvedconfig['pos'].iloc[i]
            por = self.solvedconfig['or'].iloc[i]
            self.solvedconfig['pos'].iloc[i] = [int(ppos[1]), int(ppos[3]), int(ppos[5])]
            self.solvedconfig['or'].iloc[i] = [int(por[1]), int(por[3]), int(por[5]),
                                               int(por[7]), int(por[9]), int(por[11])]
            for j in range(len(self.solvedconfig['pos'].iloc[i])):
                if self.solvedconfig['pos'].iloc[i][j] == 9:
                    self.solvedconfig['pos'].iloc[i][j] = -1
            for k in range(len(self.solvedconfig['or'].iloc[i])):
                if self.solvedconfig['or'].iloc[i][k] == 9:
                    self.solvedconfig['or'].iloc[i][k] = -1

        self.cubits = pd.read_csv("solvedconfig.txt", sep=" ")
        for i in range(len(self.cubits)):
            ppos = self.cubits['pos'].iloc[i]
            por = self.cubits['or'].iloc[i]
            self.cubits['pos'].iloc[i] = [int(ppos[1]), int(ppos[3]), int(ppos[5])]
            self.cubits['or'].iloc[i] = [int(por[1]), int(por[3]), int(por[5]),
                                        int(por[7]), int(por[9]), int(por[11])]
            for j in range(len(self.cubits['pos'].iloc[i])):
                if self.cubits['pos'].iloc[i][j] == 9:
                    self.cubits['pos'].iloc[i][j] = -1
            for k in range(len(self.cubits['or'].iloc[i])):
                if self.cubits['or'].iloc[i][k] == 9:
                    self.cubits['or'].iloc[i][k] = -1

    def checkSolved(self, type = None):
        indices = []
        if type == "edges":
            for i in range(len(self.cubits)):
                placeholder = self.cubits['pos'].iloc[i]
                if placeholder[0] == 0 or placeholder[1] == 0 or placeholder[2] == 0:
                    indices.append(i)
            for i in indices:
                for j in range(len(self.solvedconfig.iloc[i])):
                    if self.solvedconfig['pos'].iloc[i][j] != self.cubits['pos'].iloc[i][j]:
                        return False
                    if self.solvedconfig['or'].iloc[i][j] != self.cubits['or'].iloc[i][j]:
                        return False

        elif type == "corners":
            for i in range(len(self.cubits)):
                placeholder = self.cubits['pos'].iloc[i]
                if placeholder[0] != 0 and placeholder[1] != 0 and placeholder[2] != 0:
                    indices.append(i)
            for i in indices:
                for j in range(len(self.solvedconfig.iloc[i])):
                    if self.solvedconfig['pos'].iloc[i][j] != self.cubits['pos'].iloc[i][j]:
                        return False
                    if self.solvedconfig['or'].iloc[i][j] != self.cubits['or'].iloc[i][j]:
                        return False

        else:
            for i in range(len(self.solvedconfig)):
                for j in range(len(self.solvedconfig.iloc[i])):
                    if self.solvedconfig['pos'].iloc[i][j] != self.cubits['pos'].iloc[i][j]:
                        return False
                    if self.solvedconfig['or'].iloc[i][j] != self.cubits['or'].iloc[i][j]:
                        return False
        return True

    def generate_rotation_matrices(self, theta):
        #theta must be radians
        rot_x = [[1,0,0], [0,int(cos(theta)), int(-sin(theta))], [0,int(sin(theta)),int(cos(theta))]]
        rot_y = [[int(cos(theta)),0,int(sin(theta))],[0,1,0],[int(-sin(theta)),0,int(cos(theta))]]
        rot_z = [[int(cos(theta)),int(-sin(theta)),0],[int(sin(theta)),int(cos(theta)),0],[0,0,1]]
        return rot_x, rot_y, rot_z

    def move(self, dir):
        #select subset of cubits to act on -> rotate -> reorient
        indices = []
        if dir == "u":
            rot_x,rot_y,rot_z = self.generate_rotation_matrices(theta= -pi/2)
            for i in range(len(self.cubits)):
                placeholder = self.cubits['pos'].iloc[i]
                #placeholder = placeholder[i]
                if placeholder[2] == 1:
                    indices.append(i)
            for j in indices: #rotate/reorient
                ppos = self.cubits['pos'].iloc[j]
                por = self.cubits['or'].iloc[j]
                self.cubits['pos'].iloc[j] = np.matmul(rot_z,ppos)
                self.cubits['or'].iloc[j] = [por[0], por[5], por[1], por[3], por[2], por[4]]

        elif dir == "u'":
            rot_x, rot_y, rot_z = self.generate_rotation_matrices(theta=pi / 2)
            for i in range(len(self.cubits)):
                placeholder = self.cubits['pos'].iloc[i]
                if placeholder[2] == 1:
                    indices.append(i)
            for j in indices: #rotate/reorient
                ppos = self.cubits['pos'].iloc[j]
                por = self.cubits['or'].iloc[j]
                self.cubits['pos'].iloc[j] = np.matmul(rot_z,ppos)
                self.cubits['or'].iloc[j] = [por[0], por[2], por[4], por[3], por[5], por[1]]

        elif dir == "r":
            rot_x, rot_y, rot_z = self.generate_rotation_matrices(theta=-pi / 2)
            for i in range(len(self.cubits)):
                placeholder = self.cubits['pos'].iloc[i]
                if placeholder[1] == 1:
                    indices.append(i)
            for j in indices: #rotate/reorient
                ppos = self.cubits['pos'].iloc[j]
                por = self.cubits['or'].iloc[j]
                self.cubits['pos'].iloc[j] = np.matmul(rot_y,ppos)
                self.cubits['or'].iloc[j] = [por[2], por[1], por[3], por[5], por[4], por[0]]

        elif dir == "r'":
            rot_x, rot_y, rot_z = self.generate_rotation_matrices(theta=pi / 2)
            for i in range(len(self.cubits)):
                placeholder = self.cubits['pos'].iloc[i]
                if placeholder[1] == 1:
                    indices.append(i)
            for j in indices: #rotate/reorient
                ppos = self.cubits['pos'].iloc[j]
                por = self.cubits['or'].iloc[j]
                self.cubits['pos'].iloc[j] = np.matmul(rot_y,ppos)
                self.cubits['or'].iloc[j] = [por[5], por[1], por[0], por[2], por[4], por[3]]

        elif dir == "f":
            rot_x, rot_y, rot_z = self.generate_rotation_matrices(theta=-pi / 2)
            for i in range(len(self.cubits)):
                placeholder = self.cubits['pos'].iloc[i]
                if placeholder[0] == 1:
                    indices.append(i)
            for j in indices: #rotate/reorient
                ppos = self.cubits['pos'].iloc[j]
                por = self.cubits['or'].iloc[j]
                self.cubits['pos'].iloc[j] = np.matmul(rot_x,ppos)
                self.cubits['or'].iloc[j] = [por[4], por[0], por[2], por[1], por[3], por[5]]

        elif dir == "f'":
            rot_x, rot_y, rot_z = self.generate_rotation_matrices(theta=pi / 2)
            for i in range(len(self.cubits)):
                placeholder = self.cubits['pos'].iloc[i]
                if placeholder[0] == 1:
                    indices.append(i)
            for j in indices: #rotate/reorient
                ppos = self.cubits['pos'].iloc[j]
                por = self.cubits['or'].iloc[j]
                self.cubits['pos'].iloc[j] = np.matmul(rot_x,ppos)
                self.cubits['or'].iloc[j] = [por[1], por[3], por[2], por[4], por[0], por[5]]

        elif dir == "d":
            rot_x, rot_y, rot_z = self.generate_rotation_matrices(theta=pi / 2)
            for i in range(len(self.cubits)):
                placeholder = self.cubits['pos'].iloc[i]
                if placeholder[2] == -1:
                    indices.append(i)
            for j in indices: #rotate/reorient
                ppos = self.cubits['pos'].iloc[j]
                por = self.cubits['or'].iloc[j]
                self.cubits['pos'].iloc[j] = np.matmul(rot_z,ppos)
                self.cubits['or'].iloc[j] = [por[0], por[2], por[4], por[3], por[5], por[1]]

        elif dir == "d'":
            rot_x, rot_y, rot_z = self.generate_rotation_matrices(theta=-pi / 2)
            for i in range(len(self.cubits)):
                placeholder = self.cubits['pos'].iloc[i]
                if placeholder[2] == -1:
                    indices.append(i)
            for j in indices: #rotate/reorient
                ppos = self.cubits['pos'].iloc[j]
                por = self.cubits['or'].iloc[j]
                self.cubits['pos'].iloc[j] = np.matmul(rot_z,ppos)
                self.cubits['or'].iloc[j] = [por[0], por[5], por[1], por[3], por[2], por[4]]

        elif dir == "l":
            rot_x, rot_y, rot_z = self.generate_rotation_matrices(theta=pi / 2)
            for i in range(len(self.cubits)):
                placeholder = self.cubits['pos'].iloc[i]
                if placeholder[1] == -1:
                    indices.append(i)
            for j in indices: #rotate/reorient
                ppos = self.cubits['pos'].iloc[j]
                por = self.cubits['or'].iloc[j]
                self.cubits['pos'].iloc[j] = np.matmul(rot_y,ppos)
                self.cubits['or'].iloc[j] = [por[5], por[1], por[0], por[2], por[4], por[3]]

        elif dir == "l'":
            rot_x, rot_y, rot_z = self.generate_rotation_matrices(theta=-pi / 2)
            for i in range(len(self.cubits)):
                placeholder = self.cubits['pos'].iloc[i]
                if placeholder[1] == -1:
                    indices.append(i)
            for j in indices: #rotate/reorient
                ppos = self.cubits['pos'].iloc[j]
                por = self.cubits['or'].iloc[j]
                self.cubits['pos'].iloc[j] = np.matmul(rot_y,ppos)
                self.cubits['or'].iloc[j] = [por[2], por[1], por[3], por[5], por[4], por[0]]

        elif dir == "b":
            rot_x, rot_y, rot_z = self.generate_rotation_matrices(theta=pi / 2)
            for i in range(len(self.cubits)):
                placeholder = self.cubits['pos'].iloc[i]
                if placeholder[0] == -1:
                    indices.append(i)
            for j in indices: #rotate/reorient
                ppos = self.cubits['pos'].iloc[j]
                por = self.cubits['or'].iloc[j]
                self.cubits['pos'].iloc[j] = np.matmul(rot_x,ppos)
                self.cubits['or'].iloc[j] = [por[1], por[3], por[2], por[4], por[0], por[5]]

        elif dir == "b'":
            rot_x, rot_y, rot_z = self.generate_rotation_matrices(theta=-pi / 2)
            for i in range(len(self.cubits)):
                placeholder = self.cubits['pos'].iloc[i]
                if placeholder[0] == -1:
                    indices.append(i)
            for j in indices: #rotate/reorient
                ppos = self.cubits['pos'].iloc[j]
                por = self.cubits['or'].iloc[j]
                self.cubits['pos'].iloc[j] = np.matmul(rot_x,ppos)
                self.cubits['or'].iloc[j] = [por[4], por[0], por[2], por[1], por[3], por[5]]

        elif dir == "dd":
            rot_x, rot_y, rot_z = self.generate_rotation_matrices(theta=pi / 2)
            for i in range(len(self.cubits)):
                placeholder = self.cubits['pos'].iloc[i]
                if placeholder[2] == -1 or placeholder[2] == 0:
                    indices.append(i)
            for j in indices:  # rotate/reorient
                ppos = self.cubits['pos'].iloc[j]
                por = self.cubits['or'].iloc[j]
                self.cubits['pos'].iloc[j] = np.matmul(rot_z, ppos)
                self.cubits['or'].iloc[j] = [por[0], por[2], por[4], por[3], por[5], por[1]]

        elif dir == "dd'":
            rot_x, rot_y, rot_z = self.generate_rotation_matrices(theta=-pi / 2)
            for i in range(len(self.cubits)):
                placeholder = self.cubits['pos'].iloc[i]
                if placeholder[2] == -1 or placeholder[2] == 0:
                    indices.append(i)
            for j in indices:  # rotate/reorient
                ppos = self.cubits['pos'].iloc[j]
                por = self.cubits['or'].iloc[j]
                self.cubits['pos'].iloc[j] = np.matmul(rot_z, ppos)
                self.cubits['or'].iloc[j] = [por[0], por[5], por[1], por[3], por[2], por[4]]

        elif dir == "m":
            rot_x, rot_y, rot_z = self.generate_rotation_matrices(theta=-pi / 2)
            for i in range(len(self.cubits)):
                placeholder = self.cubits['pos'].iloc[i]
                if placeholder[1] == 0:
                    indices.append(i)
            for j in indices:  # rotate/reorient
                ppos = self.cubits['pos'].iloc[j]
                por = self.cubits['or'].iloc[j]
                self.cubits['pos'].iloc[j] = np.matmul(rot_y, ppos)
                self.cubits['or'].iloc[j] = [por[2], por[1], por[3], por[5], por[4], por[0]]

        elif dir == "m'":
            rot_x, rot_y, rot_z = self.generate_rotation_matrices(theta=pi / 2)
            for i in range(len(self.cubits)):
                placeholder = self.cubits['pos'].iloc[i]
                if placeholder[1] == 0:
                    indices.append(i)
            for j in indices:  # rotate/reorient
                ppos = self.cubits['pos'].iloc[j]
                por = self.cubits['or'].iloc[j]
                self.cubits['pos'].iloc[j] = np.matmul(rot_y, ppos)
                self.cubits['or'].iloc[j] = [por[5], por[1], por[0], por[2], por[4], por[3]]

        elif dir == "z":
            rot_x, rot_y, rot_z = self.generate_rotation_matrices(theta=-pi / 2)
            for j in range(len(self.cubits)):  # rotate/reorient
                ppos = self.cubits['pos'].iloc[j]
                por = self.cubits['or'].iloc[j]
                self.cubits['pos'].iloc[j] = np.matmul(rot_z, ppos)
                self.cubits['or'].iloc[j] = [por[0], por[5], por[1], por[3], por[2], por[4]]

        elif dir == "z'":
            rot_x, rot_y, rot_z = self.generate_rotation_matrices(theta=pi / 2)
            for j in range(len(self.cubits)):  # rotate/reorient
                ppos = self.cubits['pos'].iloc[j]
                por = self.cubits['or'].iloc[j]
                self.cubits['pos'].iloc[j] = np.matmul(rot_z, ppos)
                self.cubits['or'].iloc[j] = [por[0], por[2], por[4], por[3], por[5], por[1]]

        else:
            print("error: invalid direction")

    def get_color(self, por, face):
        colors = [color.blue, color.yellow, color.red,color.green,color.white,color.orange]
        i = 0
        if face == 'u':
            i = por[0]
        elif face == 'r':
            i = por[1]
        elif face == 'f':
            i = por[2]
        elif face == 'd':
            i = por[3]
        elif face == 'l':
            i = por[4]
        elif face == 'b':
            i = por[5]
        else:
            print("invalid face name")
        return colors[i]

    def search_pos(self, target):
        for i in range(len(self.cubits)):
            for j in range(len(self.cubits['pos'].iloc[0])):
                if target[j] != self.cubits['pos'].iloc[i][j]:
                    break
                if j == 2:
                    return self.cubits['or'].iloc[i]


    def show_cube(self):
        por = self.search_pos([0,0,1])
        u = box(pos=vector(0, 0, 1), color=self.get_color(por,'u'))

        por = self.search_pos([1,0,0])
        f = box(pos=vector(1, 0, 0), color=self.get_color(por,'f'))

        por = self.search_pos([0,1,0])
        r = box(pos=vector(0, 1, 0), color=self.get_color(por,'r'))

        por = self.search_pos([0,0,-1])
        d = box(pos=vector(0, 0, -1), color=self.get_color(por,'d'))

        por = self.search_pos([0,-1,0])
        l = box(pos=vector(0, -1, 0), color=self.get_color(por,'l'))

        por = self.search_pos([-1,0,0])
        b = box(pos=vector(-1, 0, 0), color=self.get_color(por,'b'))

        por = self.search_pos([-1,-1,1])
        ulb = box(pos=vector(-1,-1,1), color=self.get_color(por,'u'))
        lub = box(pos=vector(-1, -1.01, 0.99), color=self.get_color(por,'l'))
        bul = box(pos=vector(-1.01, -1, 0.99), color=self.get_color(por,'b'))

        por = self.search_pos([1, -1, 1])
        ulf = box(pos=vector(1, -1, 1), color=self.get_color(por,'u'))
        luf = box(pos=vector(1, -1.01, 0.99), color=self.get_color(por,'l'))
        ful = box(pos=vector(1.01, -1, 0.99), color=self.get_color(por,'f'))

        por = self.search_pos([1, 1, 1])
        urf = box(pos=vector(1, 1, 1), color=self.get_color(por,'u'))
        ruf = box(pos=vector(1, 1.01, 0.99), color=self.get_color(por,'r'))
        fur = box(pos=vector(1.01, 1, 0.99), color=self.get_color(por,'f'))

        por = self.search_pos([-1, 1, 1])
        urb = box(pos=vector(-1, 1, 1), color=self.get_color(por,'u'))
        rub = box(pos=vector(-1, 1.01, 0.99), color=self.get_color(por,'r'))
        bur = box(pos=vector(-1.01, 1, 0.99), color=self.get_color(por,'b'))

        por = self.search_pos([-1, -1, -1])
        dlb = box(pos=vector(-1, -1, -1), color=self.get_color(por,'d'))
        ldb = box(pos=vector(-1, -1.01, -0.99), color=self.get_color(por,'l'))
        bdl = box(pos=vector(-1.01, -1, -0.99), color=self.get_color(por,'b'))

        por = self.search_pos([1, -1, -1])
        dlf = box(pos=vector(1, -1, -1), color=self.get_color(por,'d'))
        lfd = box(pos=vector(1, -1.01, -0.99), color=self.get_color(por,'l'))
        fdl = box(pos=vector(1.01, -1, -0.99), color=self.get_color(por,'f'))

        por = self.search_pos([1, 1, -1])
        drf = box(pos=vector(1, 1, -1), color=self.get_color(por,'d'))
        rfd = box(pos=vector(1, 1.01, -0.99), color=self.get_color(por,'r'))
        frd = box(pos=vector(1.01, 1, -0.99), color=self.get_color(por,'f'))

        por = self.search_pos([-1, 1, -1])
        drb = box(pos=vector(-1, 1, -1), color=self.get_color(por,'d'))
        rbd = box(pos=vector(-1, 1.01, -0.99), color=self.get_color(por,'r'))
        brd = box(pos=vector(-1.01, 1, -0.99), color=self.get_color(por,'b'))

        por = self.search_pos([-1, 0, 1])
        ub = box(pos=vector(-1, 0, 1), color=self.get_color(por,'u'))
        bu = box(pos=vector(-1.01, 0, 0.99), color=self.get_color(por,'b'))

        por = self.search_pos([0, -1, 1])
        ul = box(pos=vector(0, -1, 1), color=self.get_color(por,'u'))
        lu = box(pos=vector(0, -1.01, 0.99), color=self.get_color(por,'l'))

        por = self.search_pos([1, 0, 1])
        uf = box(pos=vector(1, 0, 1), color=self.get_color(por,'u'))
        fu = box(pos=vector(1.01, 0, 0.99), color=self.get_color(por,'f'))

        por = self.search_pos([0, 1, 1])
        ur = box(pos=vector(0, 1, 1), color=self.get_color(por,'u'))
        ru = box(pos=vector(0, 1.01, 0.99), color=self.get_color(por,'r'))

        por = self.search_pos([-1, -1, 0])
        lb = box(pos=vector(-1, -1, 0), color=self.get_color(por,'l'))
        bl = box(pos=vector(-1.01, -0.99, 0), color=self.get_color(por,'b'))

        por = self.search_pos([1, -1, 0])
        lf = box(pos=vector(1, -1, 0), color=self.get_color(por,'l'))
        fl = box(pos=vector(1.01, -0.99, 0), color=self.get_color(por,'f'))

        por = self.search_pos([-1, 1, 0])
        rb = box(pos=vector(-1, 1, 0), color=self.get_color(por,'r'))
        br = box(pos=vector(-1.01, 0.99, 0), color=self.get_color(por,'b'))

        por = self.search_pos([1, 1, 0])
        rf = box(pos=vector(1, 1, 0), color=self.get_color(por,'r'))
        fr = box(pos=vector(1.01, 0.99, 0), color=self.get_color(por,'f'))

        por = self.search_pos([-1, 0, -1])
        db = box(pos=vector(-1, 0, -1), color=self.get_color(por,'d'))
        bd = box(pos=vector(-1.01, 0, -0.99), color=self.get_color(por,'b'))

        por = self.search_pos([1, 0, -1])
        df = box(pos=vector(1, 0, -1), color=self.get_color(por,'d'))
        fd = box(pos=vector(1.01, 0, -0.99), color=self.get_color(por,'f'))

        por = self.search_pos([0, -1, -1])
        dl = box(pos=vector(0, -1, -1), color=self.get_color(por,'d'))
        ld = box(pos=vector(0, -1.01, -0.99), color=self.get_color(por,'l'))

        por = self.search_pos([0, 1, -1])
        dr = box(pos=vector(0, 1, -1), color=self.get_color(por,'d'))
        rd = box(pos=vector(0, 1.01, -0.99), color=self.get_color(por,'r'))

    def report_cubits(self):
        merged = {"name": self.solvedconfig['name'], "pos_i": self.solvedconfig['pos'], "pos_c": self.cubits['pos'],
                  "or_i": self.solvedconfig['or'], "or_c": self.cubits['or']}
        merged = pd.DataFrame(merged)
        print(merged)

    def gen_scramble(self, n_moves):
        scramble = []
        moves = ["u","u'","r","r'","f","f'","d","d'","l","l'","b","b'"]
        for i in range(n_moves):
            n = random.randrange(0,12)
            scramble.append(moves[n])
        return scramble

    def translate(self, type, letters):
        tmoves = ["r", "u", "r'", "u'", "r'", "f", "r", "r", "u'", "r'", "u'", "r", "u", "r'", "f'"]
        lmoves = ["z", "z", "l'", "u", "u", "l", "u", "l'", "u", "u", "r", "u'", "l", "u", "r'", "z", "z"]
        rmoves = ["r", "u", "r'", "f'", "r", "u", "r'", "u'", "r'", "f", "r", "r", "u'", "r'", "u'"]
        ymoves = ["r", "u'", "r'", "u'", "r", "u", "r'", "f'", "r", "u", "r'", "u'", "r'", "f", "r"]
        moves = []
        if type == "edges":
            for letter in letters:
                if letter == "a":
                    [moves.append(l) for l in lmoves]
                elif letter == "b":
                    [moves.append(t) for t in tmoves]
                elif letter == "c":
                    [moves.append(r) for r in rmoves]
                elif letter == "e":
                    moves.append("m")
                    [moves.append(l) for l in lmoves]
                    moves.append("m'")
                elif letter == "f":
                    moves.append("l'")
                    [moves.append(t) for t in tmoves]
                    moves.append("l")
                elif letter == "g":
                    moves.append("m")
                    [moves.append(r) for r in rmoves]
                    moves.append("m'")
                elif letter == "h":
                    moves.append("dd")
                    moves.append("dd")
                    moves.append("l")
                    [moves.append(t) for t in tmoves]
                    moves.append("l'")
                    moves.append("dd")
                    moves.append("dd")
                elif letter == "j":
                    moves.append("dd'")
                    moves.append("l'")
                    [moves.append(t) for t in tmoves]
                    moves.append("l")
                    moves.append("dd")
                elif letter == "k":
                    moves.append("d'")
                    moves.append("m")
                    [moves.append(r) for r in rmoves]
                    moves.append("m'")
                    moves.append("d")
                elif letter == "l":
                    moves.append("dd")
                    moves.append("l")
                    [moves.append(t) for t in tmoves]
                    moves.append("l'")
                    moves.append("dd'")
                elif letter  == "m":
                    moves.append("m'")
                    [moves.append(r) for r in rmoves]
                    moves.append("m")
                elif letter == "n":
                    moves.append("dd")
                    moves.append("dd")
                    moves.append("l'")
                    [moves.append(t) for t in tmoves]
                    moves.append("l")
                    moves.append("dd")
                    moves.append("dd")
                elif letter == "o":
                    moves.append("m'")
                    [moves.append(l) for l in lmoves]
                    moves.append("m")
                elif letter == "p":
                    moves.append("l")
                    [moves.append(t) for t in tmoves]
                    moves.append("l'")
                elif letter == "q":
                    moves.append("l")
                    moves.append("l")
                    moves.append("d")
                    moves.append("m")
                    [moves.append(r) for r in rmoves]
                    moves.append("m'")
                    moves.append("d'")
                    moves.append("l")
                    moves.append("l")
                elif letter == "r":
                    moves.append("dd")
                    moves.append("l'")
                    [moves.append(t) for t in tmoves]
                    moves.append("l")
                    moves.append("dd'")
                elif letter == "s":
                    moves.append("d")
                    moves.append("m")
                    [moves.append(r) for r in rmoves]
                    moves.append("m'")
                    moves.append("d'")
                elif letter == "t":
                    moves.append("dd'")
                    moves.append("l")
                    [moves.append(t) for t in tmoves]
                    moves.append("l'")
                    moves.append("dd")
                elif letter == "u":
                    moves.append("m")
                    moves.append("m")
                    [moves.append(l) for l in lmoves]
                    moves.append("m")
                    moves.append("m")
                elif letter == "v":
                    moves.append("l")
                    moves.append("l")
                    [moves.append(t) for t in tmoves]
                    moves.append("l")
                    moves.append("l")
                elif letter == "w":
                    moves.append("m")
                    moves.append("m")
                    [moves.append(r) for r in rmoves]
                    moves.append("m")
                    moves.append("m")
                elif letter == "x":
                    moves.append("d")
                    moves.append("d")
                    moves.append("l")
                    moves.append("l")
                    [moves.append(t) for t in tmoves]
                    moves.append("l")
                    moves.append("l")
                    moves.append("d")
                    moves.append("d")
                else:
                    print("invalid letter")
                    print(letter)
        elif type == "corners":
            for letter in letters:
                if letter == "b":
                    moves.append("f")
                    moves.append("r'")
                    [moves.append(y) for y in ymoves]
                    moves.append("r")
                    moves.append("f'")
                elif letter =="c":
                    moves.append("f")
                    [moves.append(y) for y in ymoves]
                    moves.append("f'")
                elif letter == "d":
                    moves.append("r")
                    moves.append("d'")
                    [moves.append(y) for y in ymoves]
                    moves.append("d")
                    moves.append("r'")
                elif letter == "e":
                    moves.append("f'")
                    moves.append("d")
                    [moves.append(y) for y in ymoves]
                    moves.append("d'")
                    moves.append("f")
                elif letter == "f":
                    moves.append("d")
                    [moves.append(y) for y in ymoves]
                    moves.append("d'")
                elif letter == "g":
                    moves.append("f")
                    moves.append("d")
                    [moves.append(y) for y in ymoves]
                    moves.append("d'")
                    moves.append("f'")
                elif letter == "h":
                    moves.append("f")
                    moves.append("f")
                    moves.append("d")
                    [moves.append(y) for y in ymoves]
                    moves.append("d'")
                    moves.append("f")
                    moves.append("f")
                elif letter == "i":
                    moves.append("r'")
                    [moves.append(y) for y in ymoves]
                    moves.append("r")
                elif letter == "j":
                    [moves.append(y) for y in ymoves]
                elif letter == "k":
                    moves.append("r")
                    [moves.append(y) for y in ymoves]
                    moves.append("r'")
                elif letter == "l":
                    moves.append("r")
                    moves.append("r")
                    [moves.append(y) for y in ymoves]
                    moves.append("r")
                    moves.append("r")
                elif letter == "m":
                    moves.append("r'")
                    moves.append("f")
                    [moves.append(y) for y in ymoves]
                    moves.append("f'")
                    moves.append("r")
                elif letter == "n":
                    moves.append("d'")
                    [moves.append(y) for y in ymoves]
                    moves.append("d")
                elif letter == "o":
                    moves.append("d'")
                    moves.append("r")
                    [moves.append(y) for y in ymoves]
                    moves.append("r'")
                    moves.append("d")
                elif letter == "r":
                    moves.append("d")
                    moves.append("d")
                    [moves.append(y) for y in ymoves]
                    moves.append("d")
                    moves.append("d")
                elif letter == "s":
                    moves.append("d")
                    moves.append("f")
                    moves.append("d")
                    [moves.append(y) for y in ymoves]
                    moves.append("d'")
                    moves.append("f'")
                    moves.append("d'")
                elif letter == "t":
                    moves.append("f")
                    moves.append("f")
                    [moves.append(y) for y in ymoves]
                    moves.append("f")
                    moves.append("f")
                elif letter == "u":
                    moves.append("f'")
                    [moves.append(y) for y in ymoves]
                    moves.append("f")
                elif letter == "v":
                    moves.append("d")
                    moves.append("f'")
                    [moves.append(y) for y in ymoves]
                    moves.append("f")
                    moves.append("d'")
                elif letter == "w":
                    moves.append("d")
                    moves.append("d")
                    moves.append("f'")
                    [moves.append(y) for y in ymoves]
                    moves.append("f")
                    moves.append("d")
                    moves.append("d")
                elif letter == "x":
                    moves.append("f'")
                    moves.append("r'")
                    [moves.append(y) for y in ymoves]
                    moves.append("r")
                    moves.append("f")
        return moves

    def solve(self):
        edge_letters = []
        corner_letters = []
        counter = 0
        letter = ""
        prev_letter = ""

        edge_translations = pd.read_csv("translations_edges.txt", sep=" ")
        for i in range(len(edge_translations)):
            ptrans = edge_translations["trans"].iloc[i]
            edge_translations["trans"].iloc[i] = [int(ptrans[1]), int(ptrans[3])]
        corner_translations = pd.read_csv("translations_corners.txt", sep=" ")
        for i in range(len(corner_translations)):
            ptrans = corner_translations["trans"].iloc[i]
            corner_translations["trans"].iloc[i] = [int(ptrans[1]), int(ptrans[3]), int(ptrans[5])]

        while not self.checkSolved("edges"):
            buf_or = self.search_pos([0,1,1])
            if buf_or[0] == 0 and buf_or[1] == 1:
                indices = [i for i in range(len(edge_translations))]
                random.shuffle(indices)
                for i in indices:
                    if buf_or[0] != edge_translations["trans"].iloc[i][0] or buf_or[1] != \
                            edge_translations["trans"].iloc[i][1]:
                        letter = edge_translations["name"].iloc[i]
                        edge_letters.append(letter)
                        break

            elif buf_or[0] == 1 and buf_or[1] == 0:
                indices = [i for i in range(len(edge_translations))]
                random.shuffle(indices)
                for i in indices:
                    if buf_or[0] != edge_translations["trans"].iloc[i][0] or buf_or[1] != \
                            edge_translations["trans"].iloc[i][1]:
                        letter = edge_translations["name"].iloc[i]
                        edge_letters.append(letter)
                        break

            else:
                for i in range(len(edge_translations)):
                    if buf_or[0] == edge_translations["trans"].iloc[i][0] and buf_or[1] == \
                            edge_translations["trans"].iloc[i][1]:
                        letter = edge_translations["name"].iloc[i]
                        edge_letters.append(letter)
                        break
            prev_letter = letter
            moves = self.translate(type="edges", letters= [letter])
            for m in moves:
                self.move(m)
            self.show_cube()
            counter = counter + 1


        while not self.checkSolved("corners"):
            buf_or = self.search_pos([-1,-1,1])
            if buf_or[0] == 0 and buf_or[4] == 4 and buf_or[5] == 5:
                indices = [i for i in range(len(corner_translations))]
                random.shuffle(indices)
                for i in indices:
                    if buf_or[0] != corner_translations["trans"].iloc[i][0] or buf_or[4] != \
                            corner_translations["trans"].iloc[i][1]:
                        letter = corner_translations["name"].iloc[i]
                        corner_letters.append(letter)
                        break

            elif buf_or[0] == 4 and buf_or[4] == 5 and buf_or[5] == 0:
                indices = [i for i in range(len(corner_translations))]
                random.shuffle(indices)
                for i in indices:
                    if buf_or[0] != corner_translations["trans"].iloc[i][0] or buf_or[4] != \
                            corner_translations["trans"].iloc[i][1]:
                        letter = corner_translations["name"].iloc[i]
                        corner_letters.append(letter)
                        break

            elif buf_or[0] == 5 and buf_or[4] == 0 and buf_or[5] == 4:
                indices = [i for i in range(len(corner_translations))]
                random.shuffle(indices)
                for i in indices:
                    if buf_or[0] != corner_translations["trans"].iloc[i][0] or buf_or[4] != \
                            corner_translations["trans"].iloc[i][1]:
                        letter = corner_translations["name"].iloc[i]
                        corner_letters.append(letter)
                        break

            else:
                for i in range(len(corner_translations)):
                    if buf_or[0] == corner_translations["trans"].iloc[i][0] and buf_or[4] == \
                            corner_translations["trans"].iloc[i][1] and buf_or[5] == \
                            corner_translations["trans"].iloc[i][2]:
                        letter = corner_translations["name"].iloc[i]
                        corner_letters.append(letter)
                        break
            prev_letter = letter
            moves = self.translate(type="corners", letters= [letter])
            for m in moves:
                self.move(m)
            self.show_cube()
            counter = counter + 1

        good = []
        for i in range(len(edge_letters)):
            if i == 0 and edge_letters[0] != edge_letters[1]:
                good.append(i)
            elif i != 0 and edge_letters[i-1] != edge_letters[i]:
                good.append(i)
        edge_letters = [edge_letters[i] for i in good]
        good = []
        for i in range(len(corner_letters)):
            if i == 0 and corner_letters[0] != corner_letters[1]:
                good.append(i)
            elif i != 0 and corner_letters[i-1] != corner_letters[i]:
                good.append(i)
        corner_letters = [corner_letters[i] for i in good]

        return edge_letters, corner_letters


def main():
    rubiks = Rubiks()
    scramble = rubiks.gen_scramble(n_moves = 30)
    for s in scramble:
        rubiks.move(s)
    rubiks.show_cube()
    cont = input("continue?")
    edge_letters, corner_letters = rubiks.solve()
    print("edges:",edge_letters)
    print("corners:", corner_letters)
    rubiks.show_cube()
    print(rubiks.checkSolved("corners"))
    print(rubiks.checkSolved("edges"))
    print(rubiks.checkSolved())

