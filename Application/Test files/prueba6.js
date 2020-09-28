import React, { Component } from 'react'
import View from 'react-native'
import Meteor from 'react-native-meteor'
import Login from 'react-native-meteor-oauth'
var InterpolateHtmlPlugin = require('react-dev-utils/InterpolateHtmlPlugin');

const meteorHost = '192.168.1.73:3000' // Put your local IP here if running in dev
Meteor.connect(`ws://${meteorHost}/websocket`)

if (openBrowser('http://localhost:3000')) {
	launchEditor("prueba1.js", 10)
}

export default () => {
  return ("Data")
}
