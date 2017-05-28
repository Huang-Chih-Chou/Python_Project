# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import sqlite3
class PttPipeline(object):
	def open_spider(self, spider):
		self.conn = sqlite3.connect('myptt.sqlite')
		self.cur = self.conn.cursor()
		self.cur.execute('create table if not exists myptt(title varchar(100),url varchar(250),author varchar(50),comments text,content text,score varchar(5),date varchar(50))')
		#pass
	def close_spider(self, spider):
		# Save (commit) the changes
		self.conn.commit()
		# We can also close the connection if we are done with it.
		# Just be sure any changes have been committed or they will be lost.
		self.conn.close()
		#pass
	def process_item(self, item, spider):
		col = ','.join(item.keys())
		placeholders = ','.join(len(item) * '?')
		sql = 'insert into myptt({}) values({})'
		self.cur.execute(sql.format(col,placeholders),item.values())
		return item
