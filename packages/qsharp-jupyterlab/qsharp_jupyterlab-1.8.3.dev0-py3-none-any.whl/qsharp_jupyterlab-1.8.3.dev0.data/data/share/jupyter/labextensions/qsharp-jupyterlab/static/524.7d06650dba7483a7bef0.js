"use strict";(self.webpackChunkqsharp_jupyterlab=self.webpackChunkqsharp_jupyterlab||[]).push([[524],{524:(e,t,n)=>{n.r(t),n.d(t,{default:()=>p});var r=n(228);function a(e,t){if(!e.hasOwnProperty(t))throw new Error("Undefined state "+t+" in simple mode")}function o(e,t){(e.next||e.push)&&a(t,e.next||e.push),this.regex=function(e,t){if(!e)return/(?:)/;var n="";return e instanceof RegExp?(e.ignoreCase&&(n="i"),e=e.source):e=String(e),new RegExp("^(?:"+e+")",n)}(e.regex),this.token=function(e){if(!e)return null;if(e.apply)return e;if("string"==typeof e)return e.replace(/\./g," ");for(var t=[],n=0;n<e.length;n++)t.push(e[n]&&e[n].replace(/\./g," "));return t}(e.token),this.data=e}function i(e){return function(t,n){if(n.pending){var r=n.pending.shift();return 0==n.pending.length&&(n.pending=null),t.pos+=r.text.length,r.token}for(var a=e[n.state],o=0;o<a.length;o++){var i=a[o],s=(!i.data.sol||t.sol())&&t.match(i.regex);if(s){i.data.next?n.state=i.data.next:i.data.push?((n.stack||(n.stack=[])).push(n.state),n.state=i.data.push):i.data.pop&&n.stack&&n.stack.length&&(n.state=n.stack.pop()),i.data.indent&&n.indent.push(t.indentation()+t.indentUnit),i.data.dedent&&n.indent.pop();var d=i.token;if(d&&d.apply&&(d=d(s)),s.length>2&&i.token&&"string"!=typeof i.token){n.pending=[];for(var g=2;g<s.length;g++)s[g]&&n.pending.push({text:s[g],token:i.token[g-1]});return t.backUp(s[0].length-(s[1]?s[1].length:0)),d[0]}return d&&d.join?d[0]:d}}return t.next(),null}}function s(e,t){return function(n,r){if(null==n.indent||t.dontIndentStates&&t.doneIndentState.indexOf(n.state)>-1)return null;var a=n.indent.length-1,o=e[n.state];e:for(;;){for(var i=0;i<o.length;i++){var s=o[i];if(s.data.dedent&&!1!==s.data.dedentIfLineStart){var d=s.regex.exec(r);if(d&&d[0]){a--,(s.next||s.push)&&(o=e[s.next||s.push]),r=r.slice(d[0].length);continue e}}}break}return a<0?0:n.indent[a]}}var d=n(84),g=n(541);function u(e){e.revealed.then((()=>{const t=e.model;if("python3"===(null==t?void 0:t.defaultKernelName)){for(const e of t.cells)l(e);t.cells.changed.connect(((e,t)=>{t.newValues.forEach((e=>{l(e),e.contentChanged.connect((e=>{l(e)}))}))}))}}))}function l(e){"code"===e.type&&e.sharedModel.source.startsWith("%%qsharp")&&"text/x-qsharp"!==e.mimeType&&(e.mimeType="text/x-qsharp",console.log("updated cell mime type to text/x-qsharp"))}const p={id:"qsharp",autoStart:!0,requires:[r.IEditorLanguageRegistry,g.INotebookTracker],activate:async(e,t,n)=>{!function(e){const t=[{token:"comment",regex:/(\/\/).*/,beginWord:!1},{token:"string",regex:String.raw`^\"(?:[^\"\\]|\\[\s\S])*(?:\"|$)`,beginWord:!1},{token:"keyword",regex:String.raw`(namespace|open|import|export|as|operation|function|body|adjoint|newtype|struct|new|controlled|internal)\b`,beginWord:!0},{token:"keyword",regex:String.raw`(if|elif|else|repeat|until|fixup|for|in|return|fail|within|apply)\b`,beginWord:!0},{token:"keyword",regex:String.raw`(Adjoint|Controlled|Adj|Ctl|is|self|auto|distribute|invert|intrinsic)\b`,beginWord:!0},{token:"keyword",regex:String.raw`(let|set|use|borrow|mutable)\b`,beginWord:!0},{token:"operatorKeyword",regex:String.raw`(not|and|or)\b|(w/)`,beginWord:!0},{token:"operatorKeyword",regex:String.raw`(=)|(!)|(<)|(>)|(\+)|(-)|(\*)|(/)|(\^)|(%)|(\|)|(&&&)|(~~~)|(\.\.\.)|(\.\.)|(\?)`,beginWord:!1},{token:"meta",regex:String.raw`(Int|BigInt|Double|Bool|Qubit|Pauli|Result|Range|String|Unit)\b`,beginWord:!0},{token:"atom",regex:String.raw`(true|false|Pauli(I|X|Y|Z)|One|Zero)\b`,beginWord:!0}],n=[];for(const e of t)n.push({token:e.token,regex:new RegExp(e.regex,"g"),sol:e.beginWord}),e.beginWord&&n.push({token:e.token,regex:new RegExp(String.raw`\W`+e.regex,"g"),sol:!1});const r=function(e){a(e,"start");var t={},n=e.languageData||{},r=!1;for(var d in e)if(d!=n&&e.hasOwnProperty(d))for(var g=t[d]=[],u=e[d],l=0;l<u.length;l++){var p=u[l];g.push(new o(p,e)),(p.indent||p.dedent)&&(r=!0)}return{name:n.name,startState:function(){return{state:"start",pending:null,indent:r?[]:null}},copyState:function(e){var t={state:e.state,pending:e.pending,indent:e.indent&&e.indent.slice(0)};return e.stack&&(t.stack=e.stack.slice(0)),t},token:i(t),indent:s(t,n),languageData:n}}({start:n}),g=new d.LanguageSupport(d.StreamLanguage.define(r));e.addLanguage({name:"qsharp",mime:"text/x-qsharp",support:g,extensions:["qs"]})}(t),function(e){e.forEach((e=>{u(e)})),e.widgetAdded.connect(((e,t)=>{u(t)}))}(n)}}}}]);