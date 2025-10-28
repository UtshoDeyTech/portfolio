export const profile = {
	fullName: 'Utsho Dey',
	title: 'Software Engineer',
	institute: 'Affpilot.com',
	author_name: 'Utsho Dey', // Author name to be highlighted in the papers section
	research_areas: [
		// { title: 'Physics', description: 'Brief description of the research interest', field: 'physics' },
	],
	descriptions : 'Utsho Dey is a software engineer specializing in building exceptional digital experiences. With a passion for crafting innovative solutions, Utsho combines technical expertise with a keen eye for design to deliver high-quality software products. Whether working on web applications or mobile platforms, Utsho is dedicated to creating user-friendly interfaces and seamless functionality that enhance the overall user experience.',
}

// Set equal to an empty string to hide the icon that you don't want to display
export const social = {
	email: 'utshodey.tech@gmail.com',
	linkedin: 'https://www.linkedin.com/in/utsho-dey/',
	x: 'https://x.com/UtshoDeyTech',
	github: 'https://github.com/UtshoDeyTech',
	gitlab: '',
	scholar: 'https://scholar.google.co.in/citations?user=HMKx4rAAAAAJ&hl',
	inspire: '',
	arxiv: '',
}

export const template = {
	website_url: 'http://localhost:4321', // Astro needs to know your site’s deployed URL to generate a sitemap. It must start with http:// or https://
	menu_left: false,
	transitions: true,
	lightTheme: 'light', // Select one of the Daisy UI Themes or create your own
	darkTheme: 'dark', // Select one of the Daisy UI Themes or create your own
	excerptLength: 200,
	postPerPage: 5,
    base: '' // Repository name starting with /
}

export const seo = {
	default_title: 'Utsho Dey - Software Engineer',
	default_description: 'Utsho Dey is a software engineer specializing in building exceptional digital experiences.',
	default_image: '/images/astro-academia.png',
}
