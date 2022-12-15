module.exports = {

    devServer: {
        proxy: {
            '': {
                target: 'http://106.52.194.66/api/pages/',
                changeOrigin: true,
            },
        },
    },

    // publicPath: '',

    pwa: {
        iconPaths: {
            favicon32: 'favicon.ico',
            favicon16: 'favicon.ico',
            appleTouchIcon: 'favicon.ico',
            maskIcon: 'favicon.ico',
            msTileImage: 'favicon.ico'
        }
    }
};