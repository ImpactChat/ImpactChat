import React from 'react';


import { createMuiTheme, MuiThemeProvider } from '@material-ui/core/styles';
import { CssBaseline } from '@material-ui/core';

import { Switch, Route, BrowserRouter } from "react-router-dom";

import Login from './pages/login';
import Messages from './pages/messages';

import lightTheme from './themes/light-theme.js';
import darkTheme from './themes/dark-theme.js';


const getThemeLight = () => createMuiTheme(lightTheme);
const getThemeDark = () => createMuiTheme(darkTheme);


class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      theme: localStorage.getItem("theme") === "light" ? getThemeLight : getThemeDark,
    }
    this.toggleDarkMode = this.toggleDarkMode.bind(this);
  }

  toggleDarkMode() {
    this.setState((function(prevState) {
      if (prevState.theme === getThemeLight)
      {
        localStorage.setItem('theme', 'dark');
      } else {
        localStorage.setItem('theme', 'light');
      }
      return ({theme: prevState.theme === getThemeLight ? getThemeDark : getThemeLight});
    }))};

  render() {
      return (
        <BrowserRouter>
          <MuiThemeProvider theme={this.state.theme()}>
            <CssBaseline/>
            <Switch>
                <Route exact path={"/login"}                         render={() => <Login      toggle={this.toggleDarkMode} />} />
                <Route exact path={"/chat/messages/:channel(.*)"}    render={() => <Messages   toggle={this.toggleDarkMode} />} />
            </Switch>
          </MuiThemeProvider>
        </BrowserRouter>
    );
  }
}



// class ToggleDarkMode extends React.Component {
//     render() {
//         return (
//             <IconButton onClick={this.props.toggle} aria-label="toggleDarkMode">
//                 <Brightness4Icon fontSize="large" />
//             </IconButton>
//         );
//     }
// }
export default App;