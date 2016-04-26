import React, { PropTypes } from 'react';
import { Appbar } from 'material-components';

const App = ({ count }) => (
  <div>
    <AppBar
      title="Social Media Visualization"
      iconClassNameRight="muidocs-icon-navigation-expand-more"
    />

    <p>{count}</p>
  </div>
);

App.propTypes = {
  count: PropTypes.number.isRequired,
};

export default App;
