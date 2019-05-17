// uncomment statement below to see conosle.log output
console.log = function() {}

function eraseText(){
	console.log("Before: ", document.getElementById("memo").value)
	document.getElementById("memo").value = "";
	console.log("Clear Button Clicked");
	console.log("After: ",document.getElementById("memo").value)
}