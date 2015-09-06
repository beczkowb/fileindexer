import json

import tornado.ioloop
import tornado.web

from .database import Database

db = Database()


class Push(tornado.web.RequestHandler):
    def prepare(self):
        self.json_args = json.loads(self.request.body.decode('utf-8'))

    def post(self):
        global db 
        db.add_file(**self.json_args)
        

class Files(tornado.web.RequestHandler):
    def get(self):
        global db
        self.write(json.dumps(db.get_files()))


class Search(tornado.web.RequestHandler):
    def get(self, word):
        global db 
        self.write(json.dumps(db.search(word)))
       

app = tornado.web.Application([
    (r'/push', Push),
    (r'/files', Files),
    (r'/search/(\w+)', Search),
])


if __name__ == "__main__":
    app.listen(8000)
    tornado.ioloop.IOLoop.current().start()
