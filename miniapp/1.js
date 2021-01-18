const Towxml = require('towxml');
const towxml = new Towxml();

//Markdown转WXML
let wxml = towxml.md2wxml('# Article title');

//html转WXML
let wxml = towxml.html2wxml('<h1>Article title</h1>');

//Markdown转towxml数据
let data = towxml.toJson('# Article title','markdown');

//htm转towxml数据
let data = towxml.toJson('# Article title');