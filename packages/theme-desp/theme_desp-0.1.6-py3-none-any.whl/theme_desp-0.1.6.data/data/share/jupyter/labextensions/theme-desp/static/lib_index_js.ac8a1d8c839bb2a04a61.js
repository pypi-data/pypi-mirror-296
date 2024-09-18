"use strict";
(self["webpackChunktheme_desp"] = self["webpackChunktheme_desp"] || []).push([["lib_index_js"],{

/***/ "./lib/dark-pallette-setter.js":
/*!*************************************!*\
  !*** ./lib/dark-pallette-setter.js ***!
  \*************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   DarkPalletteSetter: () => (/* binding */ DarkPalletteSetter)
/* harmony export */ });
class DarkPalletteSetter {
    constructor() {
        this.name = 'Desp Theme Dark';
        this.type = 'dark';
    }
    setColorPallette() {
        /**
         * Borders
         */
        document.documentElement.style.setProperty('--jp-border-color0', 'var(--md-grey-200)');
        document.documentElement.style.setProperty('--jp-border-color1', 'var(--md-grey-300)');
        document.documentElement.style.setProperty('--jp-border-color2', 'var(--md-grey-400)');
        document.documentElement.style.setProperty('--jp-border-color3', 'var(--md-grey-400)');
        /**
         * Defaults use Material Design specification
         */
        document.documentElement.style.setProperty('--jp-ui-font-color0', 'rgba(255, 255, 255, 1)');
        document.documentElement.style.setProperty('--jp-ui-font-color1', 'rgba(255, 255, 255, 1)');
        document.documentElement.style.setProperty('--jp-ui-font-color2', 'rgba(255, 255, 255, 0.9)');
        document.documentElement.style.setProperty('--jp-ui-font-color3', 'rgba(255, 255, 255, 0.8)');
        /**
         * Defaults use Material Design specification
         */
        document.documentElement.style.setProperty('--jp-content-font-color0', 'rgba(255, 255, 255, 1)');
        document.documentElement.style.setProperty('--jp-content-font-color1', 'rgba(255, 255, 255, 0.9)');
        document.documentElement.style.setProperty('--jp-content-font-color2', 'rgba(255, 255, 255, 0.8)');
        document.documentElement.style.setProperty('--jp-content-font-color3', 'rgba(255, 255, 255, 0.8)');
        /**
         * Layout
         */
        document.documentElement.style.setProperty('--jp-layout-color0', '#121219');
        document.documentElement.style.setProperty('--jp-layout-color1', '#121219');
        document.documentElement.style.setProperty('--jp-layout-color2', '#0D1527');
        document.documentElement.style.setProperty('--jp-layout-color3', '#0D1527');
        document.documentElement.style.setProperty('--jp-layout-color4', '#200a58');
        /**
         * Inverse Layout
         */
        document.documentElement.style.setProperty('--jp-inverse-layout-color0', 'rgb(255, 255, 255)');
        document.documentElement.style.setProperty('--jp-inverse-layout-color1', 'rgb(255, 255, 255)');
        document.documentElement.style.setProperty('--jp-inverse-layout-color2', 'rgba(255, 255, 255, 0.87)');
        document.documentElement.style.setProperty('--jp-inverse-layout-color3', 'rgba(255, 255, 255, 0.87)');
        document.documentElement.style.setProperty('--jp-inverse-layout-color4', 'rgba(255, 255, 255, 0.87)');
        /**
         * State colors (warn, error, success, info)
         */
        document.documentElement.style.setProperty('--jp-warn-color0', 'var(--md-purple-700)');
        document.documentElement.style.setProperty('--jp-warn-color1', 'var(--md-purple-500)');
        document.documentElement.style.setProperty('--jp-warn-color2', 'var(--md-purple-300)');
        document.documentElement.style.setProperty('--jp-warn-color3', 'var(--md-purple-100)');
        /**
         * Cell specific styles
         */
        document.documentElement.style.setProperty('--jp-cell-editor-background', '#0D1527');
        document.documentElement.style.setProperty('--jp-cell-prompt-not-active-font-color', 'var(--md-grey-200)');
        /**
         * Rendermime styles
         */
        document.documentElement.style.setProperty('--jp-rendermime-error-background', '#0D1527');
        /**
         * Code mirror specific styles
         */
        document.documentElement.style.setProperty('--jp-mirror-editor-operator-color', '#a2f');
        document.documentElement.style.setProperty('--jp-mirror-editor-meta-color', '#a2f');
        document.documentElement.style.setProperty('--jp-mirror-editor-attribute-color', 'rgb(255, 255, 255)');
    }
}


/***/ }),

/***/ "./lib/index.js":
/*!**********************!*\
  !*** ./lib/index.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _style_favicon_png__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../style/favicon.png */ "./style/favicon.png");
/* harmony import */ var _style_desp_logo_png__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../style/desp-logo.png */ "./style/desp-logo.png");
/* harmony import */ var _style_destination_earth_png__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../style/destination-earth.png */ "./style/destination-earth.png");
/* harmony import */ var _style_funded_by_EU_png__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../style/funded-by-EU.png */ "./style/funded-by-EU.png");
/* harmony import */ var _style_implemented_by_png__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ../style/implemented-by.png */ "./style/implemented-by.png");
/* harmony import */ var _style_ecmwf_png__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ../style/ecmwf.png */ "./style/ecmwf.png");
/* harmony import */ var _style_esa_png__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ../style/esa.png */ "./style/esa.png");
/* harmony import */ var _style_eumetsat_png__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! ../style/eumetsat.png */ "./style/eumetsat.png");
/* harmony import */ var _light_pallette_setter__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! ./light-pallette-setter */ "./lib/light-pallette-setter.js");
/* harmony import */ var _dark_pallette_setter__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! ./dark-pallette-setter */ "./lib/dark-pallette-setter.js");











/**
 * Creates a logo, an 'img' element wrapped by a 'a' element
 */
const createLogo = (logoSrc, maxHeight, href) => {
    const logoContainer = document.createElement('a');
    logoContainer.href = href || '#';
    logoContainer.target = '_blank';
    const logo = document.createElement('img');
    logo.style.width = 'auto';
    logo.style.maxHeight = maxHeight;
    logo.style.margin = '5px';
    logo.src = logoSrc;
    logoContainer.appendChild(logo);
    return logoContainer;
};
/**
 * Changes the favicon before the application load
 */
const head = document.head;
const favicons = head.querySelectorAll('link[rel="icon"]');
favicons.forEach(favicon => head.removeChild(favicon));
const link = document.createElement('link');
link.rel = 'icon';
link.type = 'image/x-icon';
link.href = _style_favicon_png__WEBPACK_IMPORTED_MODULE_1__;
head.appendChild(link);
/**
 * Changes the tab title before the application load
 */
let title = head.querySelector('title');
if (!title) {
    title = document.createElement('title');
    head.appendChild(title);
}
title.textContent = 'Insula Code';
/**
 * Add a fixed div that display the user name
 */
const span = document.createElement('span');
span.innerText = JSON.parse(localStorage['@jupyterlab/services:UserManager#user']).name;
span.className = 'user-name-span';
document.body.appendChild(span);
/**
 * Initialization data for the theme-desp extension
 */
const plugin = {
    id: 'theme-desp:plugin',
    description: 'A JupyterLab extension.',
    autoStart: true,
    requires: [_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.IThemeManager],
    activate: (app, manager) => {
        let footerVisible = true;
        /**
         * Observes changes in the title made elsewhere in the application.
         */
        app.started.then(() => {
            Object.defineProperty(document, 'title', {
                set(arg) {
                    var _a, _b;
                    (_b = (_a = Object.getOwnPropertyDescriptor(Document.prototype, 'title'
                    // Edit the document.title property setter,
                    // call the original setter function for document.title and make sure 'this' is set to the document object,
                    // then overrides the value to set
                    )) === null || _a === void 0 ? void 0 : _a.set) === null || _b === void 0 ? void 0 : _b.call(document, 'Insula Code');
                },
                configurable: true
            });
        });
        const showFooter = () => {
            const footer = document.createElement('div');
            footer.classList.add('desp-footer');
            const logo1 = createLogo(_style_desp_logo_png__WEBPACK_IMPORTED_MODULE_2__, '36px', 'https://destination-earth.eu/');
            const logo2 = createLogo(_style_destination_earth_png__WEBPACK_IMPORTED_MODULE_3__, '40px', 'https://destination-earth.eu/');
            const logo3 = createLogo(_style_funded_by_EU_png__WEBPACK_IMPORTED_MODULE_4__, '40px', 'https://european-union.europa.eu/');
            const logo4 = createLogo(_style_implemented_by_png__WEBPACK_IMPORTED_MODULE_5__, '40px', 'https://european-union.europa.eu/');
            const logo5 = createLogo(_style_ecmwf_png__WEBPACK_IMPORTED_MODULE_6__, '40px', 'https://www.ecmwf.int/');
            const logo6 = createLogo(_style_esa_png__WEBPACK_IMPORTED_MODULE_7__, '40px', 'https://www.esa.int/');
            const logo7 = createLogo(_style_eumetsat_png__WEBPACK_IMPORTED_MODULE_8__, '40px', 'https://www.eumetsat.int/');
            const closeIcon = document.createElement('span');
            closeIcon.textContent = 'x';
            footer.appendChild(logo1);
            footer.appendChild(logo2);
            footer.appendChild(logo3);
            footer.appendChild(logo4);
            footer.appendChild(logo5);
            footer.appendChild(logo6);
            footer.appendChild(logo7);
            footer.appendChild(closeIcon);
            closeIcon.addEventListener('click', () => {
                document.body.removeChild(footer);
                footerVisible = false;
                showOpenButton();
            });
            document.body.appendChild(footer);
            footerVisible = true;
        };
        const showOpenButton = () => {
            if (document.getElementById('desp-footer-open-button'))
                return;
            const reopenButton = document.createElement('img');
            reopenButton.id = 'desp-footer-open-button';
            reopenButton.src = _style_desp_logo_png__WEBPACK_IMPORTED_MODULE_2__;
            reopenButton.classList.add('desp-footer-open-button');
            reopenButton.addEventListener('click', () => {
                document.body.removeChild(reopenButton);
                showFooter();
            });
            document.body.appendChild(reopenButton);
        };
        if (footerVisible) {
            showFooter();
        }
        else {
            showOpenButton();
        }
        /**
         * Due to the current limitation of not being able to register multiple themes
         * (https://github.com/jupyterlab/jupyterlab/issues/14202)
         * in the same extension when each theme has its own separate CSS file, we
         * handle theme variants by storing the color palette in TypeScript files and
         * loading them dynamically through a script. This approach allows us to load
         * a base theme ('theme-desp/index.css') and then override the necessary color properties
         * based on the selected palette.
         */
        const pallettesSetters = [_light_pallette_setter__WEBPACK_IMPORTED_MODULE_9__.LightPalletteSetter, _dark_pallette_setter__WEBPACK_IMPORTED_MODULE_10__.DarkPalletteSetter];
        const baseTheme = 'theme-desp/index.css';
        pallettesSetters.forEach(Pallette => {
            const pallette = new Pallette();
            manager.register({
                name: pallette.name,
                isLight: pallette.type === 'light',
                load: () => {
                    pallette.setColorPallette();
                    return manager.loadCSS(baseTheme);
                },
                unload: () => Promise.resolve(undefined)
            });
        });
    }
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (plugin);


/***/ }),

/***/ "./lib/light-pallette-setter.js":
/*!**************************************!*\
  !*** ./lib/light-pallette-setter.js ***!
  \**************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   LightPalletteSetter: () => (/* binding */ LightPalletteSetter)
/* harmony export */ });
class LightPalletteSetter {
    constructor() {
        this.name = 'Desp Theme Light';
        this.type = 'light';
    }
    setColorPallette() {
        /**
         * Borders
         */
        document.documentElement.style.setProperty('--jp-border-color0', 'var(--md-grey-400)');
        document.documentElement.style.setProperty('--jp-border-color1', 'var(--md-grey-400)');
        document.documentElement.style.setProperty('--jp-border-color2', 'var(--md-grey-300)');
        document.documentElement.style.setProperty('--jp-border-color3', 'var(--md-grey-200)');
        /**
         * Defaults use Material Design specification
         */
        document.documentElement.style.setProperty('--jp-ui-font-color0', 'rgba(0, 0, 0, 1)');
        document.documentElement.style.setProperty('--jp-ui-font-color1', 'rgba(0, 0, 0, 0.87)');
        document.documentElement.style.setProperty('--jp-ui-font-color2', 'rgba(0, 0, 0, 0.54)');
        document.documentElement.style.setProperty('--jp-ui-font-color3', 'rgba(0, 0, 0, 0.38)');
        /**
         * Defaults use Material Design specification
         */
        document.documentElement.style.setProperty('--jp-content-font-color0', 'rgba(0, 0, 0, 1)');
        document.documentElement.style.setProperty('--jp-content-font-color1', 'rgba(0, 0, 0, 0.87)');
        document.documentElement.style.setProperty('--jp-content-font-color2', 'rgba(0, 0, 0, 0.54)');
        document.documentElement.style.setProperty('--jp-content-font-color3', 'rgba(0, 0, 0, 0.38)');
        /**
         * Layout
         */
        document.documentElement.style.setProperty('--jp-layout-color0', 'white');
        document.documentElement.style.setProperty('--jp-layout-color1', 'white');
        document.documentElement.style.setProperty('--jp-layout-color2', 'var(--md-grey-200)');
        document.documentElement.style.setProperty('--jp-layout-color3', '#7B34DB');
        document.documentElement.style.setProperty('--jp-layout-color4', 'var(--md-grey-600)');
        /**
         * Inverse Layout
         */
        document.documentElement.style.setProperty('--jp-inverse-layout-color0', '#111111');
        document.documentElement.style.setProperty('--jp-inverse-layout-color1', 'var(--md-grey-900)');
        document.documentElement.style.setProperty('--jp-inverse-layout-color2', 'var(--md-grey-800)');
        document.documentElement.style.setProperty('--jp-inverse-layout-color3', 'var(--md-grey-700)');
        document.documentElement.style.setProperty('--jp-inverse-layout-color4', 'var(--md-grey-600)');
        /**
         * State colors (warn, error, success, info)
         */
        document.documentElement.style.setProperty('--jp-warn-color0', 'var(--md-purple-700)');
        document.documentElement.style.setProperty('--jp-warn-color1', 'var(--md-purple-500)');
        document.documentElement.style.setProperty('--jp-warn-color2', 'var(--md-purple-300)');
        document.documentElement.style.setProperty('--jp-warn-color3', 'var(--md-purple-100)');
        /**
         * Cell specific styles
         */
        document.documentElement.style.setProperty('--jp-cell-editor-background', 'var(--md-grey-100)');
        document.documentElement.style.setProperty('--jp-cell-prompt-not-active-font-color', 'var(--md-grey-700)');
        /**
         * Rendermime styles
         */
        document.documentElement.style.setProperty('--jp-rendermime-error-background', '#fdd');
        /**
         * Code mirror specific styles
         */
        document.documentElement.style.setProperty('--jp-mirror-editor-operator-color', '#aa22ff');
        document.documentElement.style.setProperty('--jp-mirror-editor-meta-color', '#aa22ff');
        document.documentElement.style.setProperty('--jp-mirror-editor-attribute-color', '#00c');
    }
}


/***/ }),

/***/ "./style/desp-logo.png":
/*!*****************************!*\
  !*** ./style/desp-logo.png ***!
  \*****************************/
/***/ ((module, __unused_webpack_exports, __webpack_require__) => {

module.exports = __webpack_require__.p + "19d810445d72bac9e4ca.png";

/***/ }),

/***/ "./style/destination-earth.png":
/*!*************************************!*\
  !*** ./style/destination-earth.png ***!
  \*************************************/
/***/ ((module, __unused_webpack_exports, __webpack_require__) => {

module.exports = __webpack_require__.p + "d9b215870d6ce17ae355.png";

/***/ }),

/***/ "./style/ecmwf.png":
/*!*************************!*\
  !*** ./style/ecmwf.png ***!
  \*************************/
/***/ ((module, __unused_webpack_exports, __webpack_require__) => {

module.exports = __webpack_require__.p + "3a54e5cb65a840618472.png";

/***/ }),

/***/ "./style/esa.png":
/*!***********************!*\
  !*** ./style/esa.png ***!
  \***********************/
/***/ ((module, __unused_webpack_exports, __webpack_require__) => {

module.exports = __webpack_require__.p + "0bb3f1ee1833340e6f57.png";

/***/ }),

/***/ "./style/eumetsat.png":
/*!****************************!*\
  !*** ./style/eumetsat.png ***!
  \****************************/
/***/ ((module, __unused_webpack_exports, __webpack_require__) => {

module.exports = __webpack_require__.p + "e67418ee2384fa9166d6.png";

/***/ }),

/***/ "./style/favicon.png":
/*!***************************!*\
  !*** ./style/favicon.png ***!
  \***************************/
/***/ ((module, __unused_webpack_exports, __webpack_require__) => {

module.exports = __webpack_require__.p + "4229a48410e4e10395c5.png";

/***/ }),

/***/ "./style/funded-by-EU.png":
/*!********************************!*\
  !*** ./style/funded-by-EU.png ***!
  \********************************/
/***/ ((module, __unused_webpack_exports, __webpack_require__) => {

module.exports = __webpack_require__.p + "459c48ead8e0c322064c.png";

/***/ }),

/***/ "./style/implemented-by.png":
/*!**********************************!*\
  !*** ./style/implemented-by.png ***!
  \**********************************/
/***/ ((module, __unused_webpack_exports, __webpack_require__) => {

module.exports = __webpack_require__.p + "0263dad0577ad79611d9.png";

/***/ })

}]);
//# sourceMappingURL=lib_index_js.ac8a1d8c839bb2a04a61.js.map