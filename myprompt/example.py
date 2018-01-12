# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    main.py                                            :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: rbernand <marvin@42.fr>                    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2015/08/16 10:03:01 by rbernand          #+#    #+#              #
#    Updated: 2015/08/20 21:18:58 by rbernand         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import myprompt as mp
import sys

def square(x):
    print(x*x)

def nstr(n, string):
    print(string * n)

def optional(d="coicouc"):
    print(d)

def hello():
    print("hello")

def main():
    p = mp.myPrompt(text="TaskMaster >")
    p.addCommand("exit", action=sys.exit, helper="Quit the program.")
    p.addCommand("sum", action=square, nbargs=1, transform=[int])
    p.addCommand("opt", action=optional)
    p.addCommand("print", action=nstr, nbargs=2, transform=[int, str])
    p.addCommand("print_hello", action=hello)
    p.start()

if __name__ == "__main__":
    main()
