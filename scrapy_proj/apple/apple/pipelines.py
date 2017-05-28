# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import sqlite3
class ApplePipeline(object):
	def open_spider(self, spider):
		self.conn = sqlite3.connect('apple.sqlite')
		self.cur = self.conn.cursor()
		self.cur.execute('create table if not exists apple(title varchar(100),content text,time varchar(50))')
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
		sql = 'insert into apple({}) values({})'
		self.cur.execute(sql.format(col,placeholders),item.values())
		return item
