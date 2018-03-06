'use strict';


/**
 * Gets languages supported by the server generator
 * 
 *
 * returns array
 **/
exports.serverOptions = function() {
  return new Promise(function(resolve, reject) {
    var examples = {};
    examples['*/*'] = [
  "string"
];
    if (Object.keys(examples).length > 0) {
      resolve(examples[Object.keys(examples)[0]]);
    } else {
      resolve();
    }
  });
}


/**
 * Returns options for a server framework
 * 
 *
 * framework string The target language for the server framework
 * returns object
 **/
exports.getServerOptions = function(framework) {
  return new Promise(function(resolve, reject) {
    var examples = {};
    examples['application/json'] = {
  "property1": {
    "default": "string",
    "description": "string",
    "enum": {
      "property1": "string",
      "property2": "string"
    },
    "optionName": "string",
    "type": "string"
  },
  "property2": {
    "default": "string",
    "description": "string",
    "enum": {
      "property1": "string",
      "property2": "string"
    },
    "optionName": "string",
    "type": "string"
  }
};
    if (Object.keys(examples).length > 0) {
      resolve(examples[Object.keys(examples)[0]]);
    } else {
      resolve();
    }
  });
}


/**
 * Generates a server library
 * Accepts a `GeneratorInput` options map for spec location and generation options.
 *
 * framework string framework
 * body object parameters
 * returns ResponseCode
 **/
exports.generateServerForLanguage = function(framework,body) {
  return new Promise(function(resolve, reject) {
    var examples = {};
    examples['*/*'] = {
  "code": "d40029be-eda6-4d62-b1ef-d05e2e91a72a",
  "link": "http://generator.swagger.io:80/api/gen/download/d40029be-eda6-4d62-b1ef-d05e2e91a72a"
};
    if (Object.keys(examples).length > 0) {
      resolve(examples[Object.keys(examples)[0]]);
    } else {
      resolve();
    }
  });
}

