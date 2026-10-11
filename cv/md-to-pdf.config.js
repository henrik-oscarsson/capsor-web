const path = require('path');

const root = path.join(__dirname, '..');

module.exports = {
	basedir: root,
	stylesheet: [path.join(__dirname, 'cv.css')],
	dest: path.join(root, 'CV_Henrik_Oscarsson_en.pdf'),
	pdf_options: {
		format: 'A4',
		margin: { top: '16mm', right: '16mm', bottom: '16mm', left: '16mm' },
		printBackground: true,
	},
	launch_options: {
		executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
	},
};
