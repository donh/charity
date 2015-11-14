import React, {PropTypes, Component} from 'react';
import css from '../../../node_modules/material-design-lite/material.min.css';
import withStyles from '../../decorators/withStyles';
import Button from 'material-design-react/button';

@withStyles(css)

class IntroPage extends Component {
  
  render() {
  	return (
  	  <Button colored ripple>I am colored</Button>
    );
  }

}
export default IntroPage;