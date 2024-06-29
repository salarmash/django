from datetime import timezone

from django.db import models
from django.contrib.auth.models import User


class Score(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="scores", verbose_name="کاربر")
    score = models.PositiveIntegerField(default=0, verbose_name="امتیاز")

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

    class Meta:
        verbose_name = "امتیاز"
        verbose_name_plural = "امتیازات"


class MatchDay(models.Model):
    title = models.CharField(max_length=150, verbose_name="عنوان")
    text = models.TextField(verbose_name="نوشته")
    group = models.BooleanField(default=False, verbose_name="مرحله گروهی")
    knockout = models.BooleanField(default=False, verbose_name="مرحله حذفی")
    semiFinal = models.BooleanField(default=False, verbose_name="مرحله نیمه نهایی")
    final = models.BooleanField(default=False, verbose_name="مرحله فینال")
    date = models.DateTimeField(auto_now_add=True)
    first_match_start = models.TimeField(verbose_name="زمان شروع اولین مسابقه")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "مسابقه"
        verbose_name_plural = "مسابقات"


class Match(models.Model):
    matchday = models.ForeignKey(MatchDay, on_delete=models.CASCADE, related_name="matches", verbose_name="روز بازی")
    home_name = models.CharField(max_length=100, default=" ")
    away_name = models.CharField(max_length=100, default=" ")
    home = models.CharField(max_length=2, blank=True, null=True, verbose_name="تعداد گل میزبان")
    home_img = models.ImageField(upload_to="images", blank=True, null=True, verbose_name="تصویر میزبان")
    away = models.CharField(max_length=2, blank=True, null=True, verbose_name="تعداد گل میهمان")
    away_img = models.ImageField(upload_to="images", blank=True, null=True, verbose_name="تصویر میهمان")

    def __str__(self):
        return f"{self.home_name} vs {self.away_name}"

    class Meta:
        verbose_name = "بازی"
        verbose_name_plural = "بازیها"


class UserForcast(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="forcast", verbose_name="کاربر")
    matchday = models.ForeignKey(MatchDay, on_delete=models.CASCADE, related_name="forcast", verbose_name="روز بازی")
    match = models.ForeignKey(Match, on_delete=models.CASCADE, related_name="forcast", verbose_name="بازی")
    home_name = models.CharField(max_length=100, default=" ")
    away_name = models.CharField(max_length=100, default=" ")
    home = models.CharField(max_length=2, verbose_name="تعداد گل میزبان")
    home_img = models.ImageField(upload_to="images", blank=True, null=True, verbose_name="تصویر میزبان")
    away = models.CharField(max_length=2, verbose_name="تعداد گل میهمان")
    away_img = models.ImageField(upload_to="images", blank=True, null=True, verbose_name="تصویر میهمان")

    def __str__(self):
        return f"{self.user}//{self.home_name}vs {self.away_name}//{self.home} - {self.away}"

    class Meta:
        verbose_name = "پیش بینی"
        verbose_name_plural = "پیش بینی ها"


class Rule(models.Model):
    title = models.CharField(max_length=200, verbose_name="عنوان")
    body = models.TextField(verbose_name="متن قوانین")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "مطلب"
        verbose_name_plural = "قوانین"


class UserForcastHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="history", verbose_name="کاربر")
    matchday = models.ForeignKey(MatchDay, on_delete=models.CASCADE, related_name="history", verbose_name="روز بازی")
    match = models.ForeignKey(Match, on_delete=models.CASCADE, related_name="history", verbose_name="بازی")
    home_name = models.CharField(max_length=100, default=" ")
    away_name = models.CharField(max_length=100, default=" ")
    home = models.CharField(max_length=2, verbose_name="تعداد گل میزبان")
    home_img = models.ImageField(upload_to="images", blank=True, null=True, verbose_name="تصویر میزبان")
    away = models.CharField(max_length=2, verbose_name="تعداد گل میهمان")
    away_img = models.ImageField(upload_to="images", blank=True, null=True, verbose_name="تصویر میهمان")

    def __str__(self):
        return f"{self.user}//{self.home_name}vs {self.away_name}//{self.home} -{self.away}"

    class Meta:
        verbose_name = "تاربخچه پیش بینی"
        verbose_name_plural = " تاربخچه پیش بینی ها"
