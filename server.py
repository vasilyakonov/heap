from flask import Flask, render_template
from random_word import RandomWords
import os, random
import bs4

### content generation code
colors=[]
text_file = open(u"colors.txt", "r",encoding='utf-8')
lines = text_file.read().split(',')
colors.append(lines)
r = RandomWords()
parent=[]
child=[]
paragraph=[]
bodyels=500

with open("base.html") as inf:
    txt = inf.read()
    soup = bs4.BeautifulSoup(txt,"xml")


def otherels(a):
    for i in range(bodyels):
        a=a+1
        style=bs4.BeautifulSoup(str("""<style>#mydiv"""+"%s"+""" {
      font-family: "HelveticaNeueMedium", "HelveticaNeue-Medium", "Helvetica Neue Medium", "HelveticaNeue", "Helvetica Neue", 'TeXGyreHerosRegular', "Helvetica", "Tahoma", "Geneva", "Arial", sans-serif; font-weight:500; font-stretch:normal;
      font-weight: medium;
      position: fixed;
      z-index: 9;
      background-color: %s;
      text-align: center;
      border: 10px solid %s;
      top:%svh; 
      left:%svw; 
    }

    #mydiv"""+"%d"+"""header {
      font-family: "HelveticaNeueMedium", "HelveticaNeue-Medium", "Helvetica Neue Medium", "HelveticaNeue", "Helvetica Neue", 'TeXGyreHerosRegular', "Helvetica", "Tahoma", "Geneva", "Arial", sans-serif; font-weight:500; font-stretch:normal;
      font-weight: medium;
      padding: 10px;
      cursor: move;
      z-index: 10;
      color: white;
    }</style>""") % (a,random.choice(colors[0]).lower(),random.choice(colors[0]).lower(),random.randint(0, 90),random.randint(0, 100),a),"xml")
        div=bs4.BeautifulSoup('<div id="mydiv{a}"><div id="mydiv{a}header"><p>{rand}</p></div></div>'.format(a=a, rand=r.get_random_word()),"xml")
        script=bs4.BeautifulSoup("""<script>
    //Make the DIV element draggagle:
    dragElement(document.getElementById("mydiv%s"));

    function dragElement(elmnt) {
      var pos1 = 0, pos2 = 0, pos3 = 0, pos4 = 0;
      if (document.getElementById(elmnt.id + "header")) {
        /* if present, the header is where you move the DIV from:*/
        document.getElementById(elmnt.id + "header").onmousedown = dragMouseDown;
      } else {
        /* otherwise, move the DIV from anywhere inside the DIV:*/
        elmnt.onmousedown = dragMouseDown;
      }

      function dragMouseDown(e) {
        e = e || window.event;
        e.preventDefault();
        // get the mouse cursor position at startup:
        pos3 = e.clientX;
        pos4 = e.clientY;
        document.onmouseup = closeDragElement;
        // call a function whenever the cursor moves:
        document.onmousemove = elementDrag;
      }

      function elementDrag(e) {
        e = e || window.event;
        e.preventDefault();
        // calculate the new cursor position:
        pos1 = pos3 - e.clientX;
        pos2 = pos4 - e.clientY;
        pos3 = e.clientX;
        pos4 = e.clientY;
        // set the element's new position:
        elmnt.style.top = (elmnt.offsetTop - pos2) + "px";
        elmnt.style.left = (elmnt.offsetLeft - pos1) + "px";
      }

      function closeDragElement() {
        /* stop moving when mouse button is released:*/
        document.onmouseup = null;
        document.onmousemove = null;
      }
    }
    </script>""" % a,"xml")
        soup.body.append(style)
        soup.body.append(div)
        soup.body.append(script)
        print("added {}".format(a))




### flask code

app = Flask(__name__)

@app.route('/')
def home():
   return render_template('index.html')


@app.route("/{}".format(os.environ['BOT_ENDPOINT']))
def hello():
  otherels(1)
    # save the outfile 
  with open("templates/index.html", "w",encoding='utf-8') as outf:
        outf.write(str(soup))
  print("All done!")
  return "I've changed!", 200

if __name__ == "__main__":
  app.run()