from rest_framework import serializers

from education.models import Course, Lesson, Payment


class PaymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payment
        fields = '__all__'
        #fields = ('id', 'amount', 'course', 'lesson',)


class PaymentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'


class LessonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lesson
        # fields = '__all__'
        fields = ('id', 'title', 'description', 'video_link',)


class CourseSerializer(serializers.ModelSerializer):
    lesson_count = serializers.SerializerMethodField()
    lessons_of_course = serializers.SerializerMethodField
    lessons = LessonSerializer(source='lesson_set', read_only=True, many=True)

    def get_lesson_count(self, obj):
        return Lesson.objects.filter(course=obj.id).count()

    def get_lessons_of_course(self, obj):
        return LessonSerializer(Lesson.objects.filter(course=obj), many=True).data

    class Meta:
        model = Course
        # fields = '__all__'
        fields = ('id', 'title', 'lesson_count', 'lessons')





