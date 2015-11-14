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
    const anythingSlider = {
      width: '1238px',
      height: '380px'
    };
    const anythingWindow = {
      width: '1238px',
      height: '364px'
    };
    const ulAnythingBase = {
      width: '7428px',
      left: '-2476px',
      overflow: 'visible'
    };
    const panelActivePage = {
      width: '1238px',
      height: '380px',
      overflow: 'visible',
      'z-index': 0
    };
    const photo = {
      left: '-181px'
    };

    return (
      <div className="MaterialPage">
        <div className="MaterialPage-container">
          <h1>{title}</h1>
          <p>...</p>
          <div id="container">
            <section id="home-aspot" data-action="homeAspot" data-controller="wcm" data-ga-module="aspot promo module">
              <div className="anythingSlider anythingSlider-default activeSlider" style={anythingSlider}>
                <div className="anythingWindow" style={anythingWindow}>
                  <ul className="slides anythingBase" style={ulAnythingBase}>
                    <li className="panel activePage" data-ga-module="aSpotHomePersonalPromoItem" style={panelActivePage}>
                      <img className="photo" src="/images/1600x380-Donate-Blood-button.jpg" height="380" width="1600" alt="Donate Blood through the American Red Cross" style={photo}/>
                      <div className="fixed-bg top-shadow"></div>
                        <a className="panel-link focusedLink" href="http://www.redcross.org/blood?campname=biomed&amp;campmedium=aspot_unassigned" data-ga-action="
            <c:if test='true'>Content-Homepage Aspot | Unassigned-2 | Give Blood</c:if>|Aspot_Home">
                          &nbsp;
                        </a>
                    </li>
                  </ul>
                </div>
              </div>
            </section>
          </div>
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
