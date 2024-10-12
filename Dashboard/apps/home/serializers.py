from django.apps import apps
from django.db.models import Count, Case, When,Sum
from math import floor
from django.db.models.functions import TruncMonth

def getUserType():
    my_model = apps.get_model('users', 'CustomUser')
    user_types = ['admin', 'user', 'patient', 'doctor']
    user_type_counts = my_model.objects.values('user_type').annotate(count=Count('user_type'))
    counts_dict = {user_type: 0 for user_type in user_types}
    for result in user_type_counts:
        counts_dict[result['user_type']] = result['count']
    results = [counts_dict[user_type] for user_type in user_types]
    return results


def getRateType():
    my_model = apps.get_model('evaluations', 'Review')
    rate_types = [1, 2, 3, 4,5]
    rating_counts = my_model.objects.values('rating').annotate(count=Count('rating'))
    counts_dict = {rate_type: 0 for rate_type in rate_types}
    for result in rating_counts:
        floored_rating = floor(result['rating'])  # تقريب القيمة للأسفل
        if floored_rating in counts_dict:
            counts_dict[floored_rating] = result['count']
    results = [counts_dict[rate_type] for rate_type in rate_types]
    total = my_model.objects.aggregate(total_sum=Count('comment'))
    results.append(total['total_sum'])
    return results


def getStatusType():
    my_model = apps.get_model('advertisements', 'Advertisement')
    status_types = [0,1, 2]
    status_counts = my_model.objects.values('status').annotate(count=Count('status'))
    counts_dict = {status_type: 0 for status_type in status_types}
    for result in status_counts:
        counts_dict[result['status']] = result['count']
    results = [counts_dict[status_type] for status_type in status_types]
    total = my_model.objects.filter(allowed=0).aggregate(total_sum=Count('allowed'))
    results.append(total['total_sum'])
    return results

def getAdsStatic():
    my_model = apps.get_model('advertisements', 'Advertisement')
    views_count = my_model.objects.aggregate(viewcount=Sum('views_count'))
    clicks_count = my_model.objects.aggregate(clickcount=Sum('clicks_count'))
    results=[]
    results.append(views_count["viewcount"])
    results.append(clicks_count["clickcount"])
    return results

def diseasesValid():
    my_model = apps.get_model('diseases', 'Disease')
    status_types = [0, 1]
    status_counts = my_model.objects.values('status').annotate(count=Count('status'))
    counts_dict = {status_type: 0 for status_type in status_types}
    for result in status_counts:
        counts_dict[result['status']] = result['count']
    results = [counts_dict[status_type] for status_type in status_types]
    return results

def consultationsStatus():
    my_model = apps.get_model('consultations', 'Consultation')
    status_types = [0, 1]
    status_counts = my_model.objects.values('is_complete').annotate(count=Count('is_complete'))
    counts_dict = {status_type: 0 for status_type in status_types}
    for result in status_counts:
        counts_dict[result['is_complete']] = result['count']
    results = [counts_dict[status_type] for status_type in status_types]
    return results

def postActiveDate():
    my_model = apps.get_model('posts', 'Post')
    try:
        monthly_counts = my_model.objects.annotate(month=TruncMonth('created_at')).values('month').annotate(count=Count('id')).values('month', 'count')
        counts_dict = {month: 0 for month in range(1, 13)}
        for result in monthly_counts:
            month_value = result['month']
            if month_value is not None:
                aware_month = timezone.make_aware(month_value, timezone.get_current_timezone())
                counts_dict[aware_month.month] = result['count']
        results = [counts_dict[month] for month in range(1, 13)]
    except:
        results=[0 for month in range(1, 13)]
    return results


def getdig():
    my_model = apps.get_model('diagnosis', 'DiagnosisReport')
    label_types = ['Retinal Vein Occlusion-( انسداد الوريد الشبكي)', 'Diabetic Retinopathy-( اعتلال الشبكية السكري)', 'Glaucoma-(الجلوكوما)','normal-(طبيعي)','Cataracts-(المياة البيضاء)','unkown','Stye-(دمل العين)','Pterygium-(الظفرة)','Conjunctivitis-(  التهاب الملتحمة)']
    label_type_counts = my_model.objects.values('diagnosis_result').annotate(count=Count('diagnosis_result'))
    counts_dict = {label_type: 0 for label_type in label_types}
    for result in label_type_counts:
        counts_dict[result['diagnosis_result']] = result['count']
    results = [counts_dict[label_type] for label_type in label_types]
    return results


def doAll():
    user_type_counts=getUserType()
    rating_counts=getRateType()
    ads_status=getStatusType()
    ads_statics=getAdsStatic()
    diseases=diseasesValid()
    cons_status=consultationsStatus()
    posts_date=postActiveDate()
    diagnosis_result=getdig()
    response_data = {
    "UserCounts": user_type_counts,
    "Rating": rating_counts,
    "Ads_status": ads_status,
    "Ads_static": ads_statics,
    "Diseases": diseases,
    "Cons_status": cons_status,
    "Posts_date": posts_date,
    "Diagnosis_result": diagnosis_result
    }
    return response_data