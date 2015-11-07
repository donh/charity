/*! React Starter Kit | MIT License | http://www.reactstarterkit.com/ */

import React, { PropTypes, Component } from 'react';
import styles from './MaterialPage.css';
import withStyles from '../../decorators/withStyles';

@withStyles(styles)
class MaterialPage extends Component {

  static contextTypes = {
    onSetTitle: PropTypes.func.isRequired,
  };

  render() {
    const title = 'Sophia Foundation';
    this.context.onSetTitle(title);
    return (
      <div className="MaterialPage">
        <div className="MaterialPage-container">
          <h1>{title}</h1>
          <p>...</p>
          <div class="styleguide-demo">
            <h1>Typography</h1>
            <iframe src="./typography/demo.html" scrolling="no"></iframe>
          </div>

          <div class="styleguide-demo">
            <h1>List</h1>
            <iframe src="./list/demo.html" scrolling="no"></iframe>
          </div>

          <div class="styleguide-demo">
            <h1>Palette</h1>
            <iframe src="./palette/demo.html" scrolling="no"></iframe>
          </div>

          <div class="styleguide-demo">
            <h1>Shadows</h1>
            <iframe src="./shadow/demo.html" scrolling="no"></iframe>
          </div>

          <div class="styleguide-demo">
            <h1>Cards</h1>
            <iframe src="./card/demo.html" scrolling="no"></iframe>
          </div>

          <div class="styleguide-demo">
            <h1>Animation</h1>
            <iframe src="./animation/demo.html" scrolling="no"></iframe>
          </div>

          <div class="styleguide-demo">
            <h1>Button</h1>
            <iframe src="./button/demo.html" scrolling="no"></iframe>
          </div>

          <div class="styleguide-demo">
            <h1>Menu</h1>
            <iframe src="./menu/demo.html" scrolling="no"></iframe>
          </div>

          <div class="styleguide-demo">
            <h1>Text Field</h1>
            <iframe src="./textfield/demo.html" scrolling="no"></iframe>
          </div>

          <div class="styleguide-demo">
            <h1>Radio Buttons</h1>
            <iframe src="./radio/demo.html" scrolling="no"></iframe>
          </div>

          <div class="styleguide-demo">
            <h1>Checkbox</h1>
            <iframe src="./checkbox/demo.html" scrolling="no"></iframe>
          </div>

          <div class="styleguide-demo">
            <h1>Switch</h1>
            <iframe src="./switch/demo.html" scrolling="no"></iframe>
          </div>

          <div class="styleguide-demo">
            <h1>Icon Toggle</h1>
            <iframe src="./icon-toggle/demo.html" scrolling="no"></iframe>
          </div>

          <div class="styleguide-demo">
            <h1>Slider</h1>
            <iframe src="./slider/demo.html" scrolling="no"></iframe>
          </div>

          <div class="styleguide-demo">
            <h1>Spinner</h1>
            <iframe src="./spinner/demo.html" scrolling="no"></iframe>
          </div>

          <div class="styleguide-demo">
            <h1>Progress Bar</h1>
            <iframe src="./progress/demo.html" scrolling="no"></iframe>
          </div>

          <div class="styleguide-demo">
            <h1>Layout</h1>
              <iframe src="./layout/demo.html" scrolling="no"></iframe>
          </div>

          <div class="styleguide-demo">
            <h1>Content Tabs</h1>
            <iframe src="./tabs/demo.html" scrolling="no"></iframe>
          </div>

          <div class="styleguide-demo">
            <h1>Icons</h1>
            <iframe src="./icons/demo.html" scrolling="no"></iframe>
          </div>


          <div class="styleguide-demo">
            <h1>Tooltip</h1>
            <iframe src="./tooltip/demo.html" scrolling="no"></iframe>
          </div>

          <div class="styleguide-demo">
            <h1>Column Layout</h1>
              <iframe src="./column-layout/demo.html"></iframe>
          </div>

          <div class="styleguide-demo">
            <h1>Footer</h1>
              <iframe src="./footer/demo.html"></iframe>
          </div>
        </div>
      </div>
    );
  }

}

export default MaterialPage;
