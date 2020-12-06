# -*- coding: utf-8 -*-

from sys import argv
from pickle import dump
from pickle import load
from os import chdir as cd
from os import system

file_name = "/Users/sm/git_config.bin"

def git_update (conf):
	try:
		cd(conf[1])
		system("git init")
		system("git add .")
		system("git commit -m 'V {}'".format(conf[3]))
		system("git remote add origin https://github.com/{}/{}.git".format(conf[0], conf[2]))
		system("git push -u origin master")
	except FileNotFoundError:
		print("\n\t[-] Error! File not found! Recreate config!\n")
		return 0
	
	print("\n\t[+] Complite! Project succsessfully uploaded!\n")
		

def create_file ():
	print("\n\t[*] Creating new file {}\n".format(file_name))

	with open(file_name, "w+b") as file:
		dump(input("User >> "), file)
		dump(input("Full Path >> "), file)
		dump(input("Project name >> "), file)
		dump(input("Version >> "), file)

	print("\n\t[+] Complite! File {} was successfully created!\n".format(file_name))

def load_conf ():
	try:
		with open(file_name, "r+b") as file:
			user = load(file)
			path = load(file)
			project = load(file)
			version = load(file)
	except IOError:
		print("\n\t[-] Error! File {} not found!\n".format(file_name))
		create_file()
		[user, path, project, version] = load_conf()
	
	return [user, path, project, version]

def main ():
	try:
		if argv[1] == "-l":
			git_update(load_conf())
		elif argv[1] == "-c":
			create_file()
			git_update(load_conf())
		else:
			raise IndexError
	except IndexError:
		print("-l -> load user's config\n-c -> create new user's config")

if __name__ == '__main__':
	main()
