import Aura from '@primevue/themes/aura';
import { definePreset } from "@primevue/themes";

const Theme = definePreset(Aura, {
    semantic: {
        primary: {
            50: '#4da8c5',
            100: '#2998b4',
            200: '#183059',
            300: '#183059',
            400: '#183059',
            500: '#183059',
            600: '#16294d',
            700: '#14243f',
            800: '#101f31',
            900: '#0e1a24',
            950: '#0a1319'
        }/*,
        secondary: {
            50: '#E3F8FF',
            100: '#B3ECFF',
            200: '#81DEFD',
            300: '#5ED0FA',
            400: '#57B8FF',
            500: '#009EFA',
            600: '#0087D5',
            700: '#006BA8',
            800: '#00507A',
            900: '#003B5A',
            950: '#003B5A'
        }*/
    },
    components: {
        card: {
            colorScheme: {
                light: {
                    root: {
                        background: '{surface.50}',
                        color: '#57B8FF'
                    },
                    subtitle: {
                        color: '#57B8FF'
                    }
                },
                dark: {
                    root: {
                        background: '{surface.900}',
                        color: '#57B8FF'
                    },
                    subtitle: {
                        color: '#57B8FF'
                    }
                }
            }
        }
    },
    colors: {
        'p-green-50': '#E3F8FF',
        'p-green-100': '#B3ECFF',
        'p-green-200': '#81DEFD',
        'p-green-300': '#5ED0FA',
        'p-green-400': '#57B8FF',
        'p-green-500': '#009EFA',
        'p-green-600': '#0087D5',
        'p-green-700': '#006BA8',
        'p-green-800': '#00507A',
        'p-green-900': '#003B5A'
    }
});

export default Theme;
