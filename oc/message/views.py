from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render 
from django.http import JsonResponse
from django.views.generic import TemplateView
from django.db.models import Q
from friend.models import Friend
from .models import Message



# def ChatView(request, id=None):
# 	fr = Friend.objects.filter(fid=id)
# 	curr_user = request.user.profile.id
# 	msg_list = Message.objects.filter((Q(sender_profile_id=curr_user)&Q(reciever_profile_id=id))|(Q(sender_profile_id=id)&Q(reciever_profile_id=curr_user)))
# 	msg_list1 = msg_list.filter(reciever_profile_id=curr_user)
# 	msg_list1.update(seen_status=True)
# 	return render(request, "message/chatpage.html", {
# 		'friend_name':fr[0].name,
# 		'friend_pro_id':fr[0].fid,
# 		'msg_list':msg_list,
# 		})

def ChatView(request, id=None):
	fr = Friend.objects.filter(fid=id)
	curr_user = request.user.profile.id
	msg_list = Message.objects.filter((Q(sender_profile_id=curr_user)&Q(reciever_profile_id=id))|(Q(sender_profile_id=id)&Q(reciever_profile_id=curr_user)))
	msg_list1 = msg_list.filter(reciever_profile_id=curr_user)
	msg_list1.update(seen_status=True)

	paginator = Paginator(msg_list, 7) # Show 7 contacts per page

	page = request.GET.get('page')
	try:
		msg_list_piece = paginator.page(page)
	except PageNotAnInteger:
		# If page is not an integer, deliver first page.
		msg_list_piece = paginator.page(1)
	except EmptyPage:
		# If page is out of range (e.g. 9999), deliver last page of results.
		msg_list_piece = paginator.page(paginator.num_pages)
	return render(request, "message/chatpage.html", {
		'friend_name':fr[0].name,
		'friend_pro_id':fr[0].fid,
		'msg_list':msg_list_piece,
		})


def SaveView(request):
	if request.is_ajax():
		try:
			
			msg = request.POST.get('chat-msg','')
			reciever_profile_id = request.POST.get('rec_id','')
		
			m = Message(

					msg=msg,
					sender_profile_id=request.user.profile.id,
					sender_name=request.user.first_name+" "+request.user.first_name,
					reciever_profile_id=reciever_profile_id,
					
				)
			m.save()
			data={
				'message':msg
			}
			return JsonResponse(data)
		except:
			return JsonResponse({'error':'error in sending'}, status=400)


class UnseenView(TemplateView):
	template_name = 'message/unseen.html'
	def get_context_data(self, **kwargs):
		context = super(UnseenView, self).get_context_data(**kwargs)
		context['msg_list'] = Message.objects.filter(Q(reciever_profile_id=self.request.user.profile.id)&Q(seen_status=False))

		return context