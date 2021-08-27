var reverseString = function(s, n=0) {
    if (n == Math.floor(s.length/2)){
        console.log(s);
        return;
    }
    var temp = s[n];
    s.splice(n,1,s[s.length-1-n]);
    s.splice(s.length-1-n,1,temp);
    console.log(s);
    reverseString(s, n+1);
};

reverseString(['h','e','l','l','o'])



// 1 2 3 4
// 1
// 2 3 4
// 1 3 4
// 2 1 3 4