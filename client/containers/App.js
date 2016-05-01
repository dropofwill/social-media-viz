import React, { PropTypes, Component } from 'react';
import { Appbar } from 'material-components';

class App extends Component {

  getChildContext() {
    return {
      componentStyle: {
        primaryColor: '#009688',
        primaryFontColor: '#FFFFFF',
        secondaryColor: '#00796b',
        secondaryFontColor: 'rgba(255, 255, 255, 0.9)',
        errorColor: '#C00',
        successColor: '#00796b',
        typographyColor: '#212121',
      },
    };
  }

  render() {
    return (
      <div>
        <Appbar fixed>
          <Appbar.Title>Social Media Visualization</Appbar.Title>
        </Appbar>

        <p>{this.props.count}</p>
      </div>
    );
  }
}

App.propTypes = {
  count: PropTypes.number.isRequired,
};

App.childContextTypes = {
  componentStyle: React.PropTypes.object,
};

export default App;
