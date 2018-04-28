from gimpfu import *
import os
import time
import tempfile

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import SocketServer

class Handler(BaseHTTPRequestHandler):

    def __init__(self, img,*args):
        self.img = img
        self.name = "texture.bmp"
        BaseHTTPRequestHandler.__init__(self, *args)
    
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'image/bmp')
        self.end_headers()

    def do_GET(self):
        self._set_headers()
        path = os.path.join(tempfile.gettempdir(), self.name)
        getPicture(self.img, path, self.name)
        f = open(path, 'rb')
        self.wfile.write(f.read())
        f.close()
        
def run(img):
    server_address = ('', 1337)
    def handler(*args):
        Handler(img, *args)
    daemon = HTTPServer(server_address, handler)
    daemon.serve_forever()

def getPicture(img,path,name):
    new_image = img.duplicate()
    layer = pdb.gimp_image_merge_visible_layers(new_image, CLIP_TO_IMAGE)
    pdb.file_bmp_save(new_image, layer, path, name)
    pdb.gimp_image_delete(new_image)
    time.sleep(0.02)

def start_stream(img, layer):
    import pygtk
    pygtk.require('2.0')
    import gimpui
    import gtk
    progress = gimpui.ProgressBar()
    progress.show()
    run(img)
    return

register(
    "texture-streamer",
    "Streams the current image on port 1337",
    "This plugin will stream the current image on port 1337, it can be used with the Open-Volt car renderer.",
    "Olfillas Odikno",
    "Olfillas Odikno",
    "2018",
    "Start Open-Volt Server",
    "*",
    [
        (PF_IMAGE, "img", "Image", None),
        (PF_LAYER, "layer", "Layer", None)
    ],
    [],
    start_stream, menu="<Image>/File/")
main()