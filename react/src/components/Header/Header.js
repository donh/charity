/*! React Starter Kit | MIT License | http://www.reactstarterkit.com/ */

import React, { Component } from 'react';
import styles from './Header.css';
import withStyles from '../../decorators/withStyles';
import Link from '../Link';
import Navigation from '../Navigation';

@withStyles(styles)

class Header extends Component {
  render() {
    const divStyle = {
      backgroundColor: 'white'
    };
    return (
      <div className="Header">
        <header className="mdl-layout__header">
          <div className="mdl-layout__header-row" style = {divStyle}>
            <img className="Header-brand" src={require('./redcross.png')} />
          </div>
          <div className="mdl-layout__header-row">
            <span className="mdl-layout-title">Sophia Project</span>
            <div className="mdl-layout-spacer"></div>
            <nav className="mdl-navigation mdl-layout--large-screen-only">
              <a className="mdl-navigation__link" href="">我要捐款</a>
              <a className="mdl-navigation__link" href="">我要捐血</a>
              <a className="mdl-navigation__link" href="">怎麼幫助</a>
              <a className="mdl-navigation__link" href="">取得協助</a>
            </nav>
          </div>
        </header>
        <div className="Header-container">
          <a className="Header-brand" href="/" onClick={Link.handleClick}>
            <img className="Header-brandImg" src={require('./logo-small.png')} width="38" height="38" alt="React" />
            <span className="Header-brandTxt">Sophia Foundation</span>
          </a>
          <Navigation className="Header-nav" />
          <div className="Header-banner">
            <h1 className="Header-bannerTitle">React</h1>
            <p className="Header-bannerDesc">Complex web apps made easy</p>
          </div>
        </div>
      </div>
    );
  }

}

export default Header;
