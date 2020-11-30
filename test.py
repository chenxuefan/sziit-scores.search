def application(env,start_response):
	start_response('200 OK',[{'Conten-Type','text/html'}])
	return ['hello world!']
