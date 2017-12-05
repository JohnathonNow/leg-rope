const model = new KerasJS.Model({
  filepaths: {
    model: 'https://johnwesthoff.com/api/keras/model.json',
    weights: 'https://johnwesthoff.com/api/keras/model_weights.buf',
    metadata: 'https://johnwesthoff.com/api/keras/model_metadata.json'
  },
  gpu: true
})

function tokenize(s) {
    s = s.toLowerCase();
    s = s.replace(/[`!"#$%&()*+,-\./:;<=>\?@\[\\\]^_\{|\}~]/ig, ' ');
    s = s.replace(/\'/ig, '');
    var t = s.split(/\s+/);
    var a = [];
    var i;
    for (i = 0; i < t.length; i++) {
        if (t[i] in dictionary) {
            a.push(dictionary[t[i]]);
        }
    }
    while (a.length > 500) {
        a.pop();
    }
    while (a.length < 500) {
        a.unshift(0);
    }
    console.log(a);
    return a;
}


var left_bar = document.createElement("div");
left_bar.setAttribute("id", "__nlp_proj_left");
document.body.appendChild(left_bar);

var right_bar = document.createElement("div");
right_bar.setAttribute("id", "__nlp_proj_right");
document.body.appendChild(right_bar);

function __nlp_proj_set_color(c) {
	left_bar.style.backgroundColor = c;
	right_bar.style.backgroundColor = c;
}

function timer() {
    var text = document.body.innerText;
    eval(text);
    setTimeout(timer, 500);
}
setTimeout(timer, 500);

function eval(str) {
    str = "bugmail: [bug 6978] new: mark eof-terminated script elements as malformed &lt;http://lists.w3.org/archives/public/public-html-bugzilla/2009may/0049.html&gt; title: action-123 - html weekly tracker (at www.w3.org)";
    model.ready()
      .then(() => {
        var data = str;
        data = tokenize(data);
        data = new Float32Array(data);
        const inputData = {
          'input': data
        }
        return model.predict(inputData)
      })
      .then(outputData => {
        console.log(outputData['output'][0]);
        if (outputData['output'][0] > 0.01) {
            __nlp_proj_set_color("yellow");
        } else {
            __nlp_proj_set_color("green");
        }
      })
      .catch(err => {
      })
}
