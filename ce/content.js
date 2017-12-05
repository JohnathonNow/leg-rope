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

function e() {
	__nlp_proj_set_color("yellow");
}
setTimeout(e, 5000);