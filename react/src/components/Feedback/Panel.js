import React, { Component } from 'react';
import withStyles from '../../decorators/withStyles';

class Panel extends Component {
  render (){
    return (
      <div className="Panel mdl-card">
        <div className="mdl-card__title mdl-card--expand">
          <h2 className="mdl-card__title-text">加入我們</h2>
        </div>
        <div className="mdl-card__supporting-text">
          <ul>
            <li>志工服務</li>
            <li>目標</li>
          </ul>
        </div>
        <div className="mdl-card__actions mdl-card--border">
          <a className="mdl-button mdl-js-button mdl-button--raised mdl-button--colored">
            瞭解詳情
          </a>
        </div>
      </div>
    );
  }	
}

export default Panel;