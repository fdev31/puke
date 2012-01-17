load('env.rhino.js');
load('jasmine/jasmine.js')
load('jasmine/jasmine-html.js')
load('jquery/jquery-1.7.js')
//load('jasmine-jquery/jasmine-jquery.js')
//load('jasmine-ajax/mock-ajax.js')
//load('jasmine-ajax/spec-helper.js')

Envjs.scriptTypes['text/javascript'] = true;
Envjs.scriptTypes['text/envjs'] = true;
Envjs.scriptTypes[''] = true;

var specFile;

jQuery.support.cors = true;
for (i = 0; i < arguments.length; i++) {
    specFile = arguments[i];


    console.log("Loading: " + specFile);

    window.location = specFile
}
