#coding=utf-8
# python3.6
import sys
import os
import os.path

suffixList = ['.rar', '.zip', '.sql', '.gz', '.tar', '.ba2', '.tar.bz2', '.bak', '.dat', '.txt', '.mdb', '.doc', '.lst', '.tmp', '.temp', '.xml']
keyList = ['web', 'webroot', 'WebRoot', 'website', 'www', 'wwww', 'www1', 'www2', 'www3', 'www4', 'www5', 'default', 'log', 'elk', 'weblog',
 'mysql', 'ftp', 'FTP', 'MySQL', 'redis', 'Redis', 'sa', 'cig', 'access', 'error', 'logs', 'data', 'database', 'sql', 'vpn', 'proxy', 'temp']


def use_url_guess(url):
	"""
	根据URL，推测一些针对性的文件名
	:param url: 想要推测的URL
	:return: null
	"""
	num1 = url.find('.')
	num2 = url.find('.', num1 + 1)
	keyList.append(url[num1 + 1:num2])
	keyList.append(url[num1 + 1:num2].upper())
	keyList.append(url)  # 如www.hack.com
	keyList.append(url.upper())
	keyList.append(url.replace('.', '_'))  # www_hack_com
	keyList.append(url.replace('.', '_').upper())
	keyList.append(url.replace('.', ''))  # wwwhackcom
	keyList.append(url.replace('.', '').upper())
	keyList.append(url[num1 + 1:])  # hack.com
	keyList.append(url[num1 + 1:].upper())
	keyList.append(url[num1 + 1:].replace('.', '_'))  # hack_com
	keyList.append(url[num1 + 1:].replace('.', '_').upper())


def combination_url(keyList, suffixList):
	"""
	组合猜解URL
	:param keyList: 猜解的文件名
	:param suffixList: 猜解的后缀
	:return:组合完的列表
	"""
	tmpList = []
	for key in keyList:
		for suff in suffixList:
			tmpList.append(key + suff)
	return tmpList


# dic 路径
MAINPATH = str('./dic/')
# MAINPATH = ''


def main():
	url = input("[>] Please input (e.g:www.hack.com):\n[>] ")
	script = int(input("[>] 输入数字选择脚本 1 asp、2 aspx、3 php、4、jsp: \n[>] "))
	use_url_guess(url)

	combination_urls = combination_url(keyList, suffixList)

	fobj_file = str(MAINPATH + "keyFiles.txt")
	fobj = open(fobj_file, 'w')
	for each in combination_urls:
		fobj.write('%s%s' % (each, '\n'))
		fobj.flush()

	def write_files(hz, outfile):
		"""
		获取输入的后缀类型，将对应字典输出到文件
		:param hz: 输入后缀,str类型
		:param outfile: 输出的文件对象
		"""
		file_path = str(MAINPATH + "dic/" + hz + ".txt")
		f = open(file_path, 'r', encoding='gbk')
		for s in f.readlines():
			outfile.write(s)
	if script == 1:
		write_files('asp', fobj)
	if script == 2:
		write_files('aspx', fobj)
	if script == 3:
		write_files('php', fobj)
	if script == 4:
		write_files('jsp', fobj)

	# 输出目录名到生成的文件
	f_path = MAINPATH + 'dic/dir.txt'
	f= open(f_path, 'r', encoding='gbk')
	for s in f.readlines():
		fobj.write(s)

	print("[+] dic is OK \n[+] Please cat keyFiles.txt")



if __name__ == '__main__':
	main()



