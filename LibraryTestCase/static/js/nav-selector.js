let currentUrl = window.location.pathname;
let nav = document.getElementById('nav-bar');


for (let i = 0; i < nav.children.length; i++) {
	let elem = nav.children[i].children[0];
	if (currentUrl == elem.pathname) {
		elem.className = "btn btn-primary";
		console.log();
	};
};
