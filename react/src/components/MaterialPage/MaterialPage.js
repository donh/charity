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
          <div id="container">
            <section id="home-aspot" data-action="homeAspot" data-controller="wcm" data-ga-module="aspot promo module">
              <div className="anythingSlider anythingSlider-default activeSlider">
                <div className="anythingWindow">
                  <ul className="slides anythingBase ulAnythingBase">
                    <li className="panel activePage panelActivePage" data-ga-module="aSpotHomePersonalPromoItem">
                      <img className="photo" src="/images/1600x380-Donate-Blood-button.jpg" height="380" width="1600" alt="Donate Blood through the American Red Cross"/>
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
        </div>
      </div>
    );
  }

}

export default MaterialPage;
