import { client } from '../hooks/exposeAuth';
import { unref } from 'vue';

export async function uploadFile(file: any, url: any, auth: any) {
	// set up the request data
	let formData = new FormData()
	formData.append('file', file.file)

	// track status and upload file
	file.status = 'loading'
	let response;
	if (auth)
	{
		const cli = unref(client);
		if (!cli) throw new Error('Unable to acquire Auth0 client');
		const token = await cli.getAccessTokenSilently();

		response = await fetch(url, { method: 'POST', body: formData, headers: {
			Authorization: 'Bearer ' + token
		  } })
	}
	else
	{
		response = await fetch(url, { method: 'POST', body: formData })
	}

	// change status to indicate the success of the upload request
	file.status = response.ok

	return response
}

export function uploadFiles(files: any, url: any, auth: any) {
	return Promise.all(files.map((file: any) => uploadFile(file, url, auth)))
}

export default function createUploader(url: any, auth: any) {
	return {
		uploadFile: function (file: any) {
			return uploadFile(file, url, auth)
		},
		uploadFiles: function (files: any) {
			return uploadFiles(files, url, auth)
		},
	}
}