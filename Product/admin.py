from django.contrib import admin
from Product.models import *
from django import forms
from datetime import datetime
from Configuration.admin import make_active, make_deactive
from django.forms.utils import ErrorList

# from AdroitInventry.admin_validation import CityMasterForm, CountryMasterForm, StateMasterForm
from rangefilter.filter import DateRangeFilter, DateTimeRangeFilter
import xlwt
from django.http import HttpResponse


def export_xls(modeladmin, request, queryset):
    import xlwt

    response = HttpResponse(content_type="application/ms-excel")
    response["Content-Disposition"] = "attachment; filename=ProductReport.xls"
    wb = xlwt.Workbook(encoding="utf-8")
    ws = wb.add_sheet("ProductReport")

    row_num = 0

    columns = [
        ("S.No", 2000),
        ("Product Id", 1000),
        ("Product Category", 4000),
        ("Product", 6000),
        ("Food Type", 2000),
        ("Company", 3000),
        ("Product Description", 8000),
        ("Price", 2000),
        ("Discount Price", 2000)

    ]

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num][0], font_style)
        # set column width
        ws.col(col_num).width = columns[col_num][1]

    font_style = xlwt.XFStyle()
    font_style.alignment.wrap = 1

    for obj in queryset:
        v_details = obj.variant_deatils
        if v_details != None:
            for i in v_details:
                v_q_id = Variant.objects.filter(variant=i["name"])[0].id
                i["v_id"] = v_q_id
        else:
            pass
        row_num += 1
        row = [
            row_num,
            obj.id,
            obj.product_category.category_name,
            obj.product_name,
            obj.food_type.food_type,
            obj.Company.company_name,
            obj.product_desc,
            obj.price,
            obj.discount_price,
            str(v_details),
        ]
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response


export_xls.short_description = "Export Selected to XLS"


def addon_settings(modeladmin, request, queryset):
    for i in queryset:
        addons = i.associated_addons
        cid = i.Company_id
        if addons != None:
            for j in addons:
                q = Addons.objects.filter(
                    Company=cid, name=j["addon_name"], addon_group=i.id
                )
                if q.count() == 0:
                    q_create = Addons.objects.create(
                        Company_id=cid,
                        name=j["addon_name"],
                        addon_group_id=i.id,
                        addon_amount=j["price"],
                    )
                else:
                    q_update = q.update(
                        name=j["addon_name"],
                        addon_group_id=i.id,
                        addon_amount=j["price"],
                    )
        else:
            pass


addon_settings.short_description = "Manage Associated Addons"


class CategoryMasterAdmin(admin.ModelAdmin):
    # form = CountryMasterForm
    exclude = [
        # 'status',
        "active_status",
        "created_at",
        "updated_at",
    ]

    list_filter = [
        "active_status",
        ("created_at", DateRangeFilter),
        ("updated_at", DateRangeFilter),
        "Company__company_name",
    ]

    search_fields = [
        "category_name",
    ]

    list_display = [
        "category_name",
        "Company",
        "active_status",
        "created_at",
    ]

    actions = [make_active, make_deactive]
    list_display_links = None
    list_per_page = 10

    def has_delete_permission(self, request, obj=None):
        return True

    def has_add_permission(self, request, obj=None):
        return False

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_at = datetime.now()
        else:
            obj.updated_at = datetime.now()
        obj.save()


class SubCategoryMasterAdmin(admin.ModelAdmin):
    # form = CountryMasterForm
    exclude = [
        # 'status',
        "active_status",
        "created_at",
        "updated_at",
    ]

    list_filter = [
        "category__category_name",
        "active_status",
        ("created_at", DateRangeFilter),
        ("updated_at", DateRangeFilter),
    ]

    search_fields = [
        "subcategory_name",
    ]

    list_display = [
        "category",
        "subcategory_name",
        "active_status",
        "created_at",
    ]
    list_display_links = None
    actions = [make_active, make_deactive]

    list_per_page = 10

    def has_delete_permission(self, request, obj=None):
        return True

    def has_add_permission(self, request, obj=None):
        return False

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_at = datetime.now()
        else:
            obj.updated_at = datetime.now()
        obj.save()


class FoodTypeMasterAdmin(admin.ModelAdmin):
    # form = CountryMasterForm
    exclude = [
        # 'status',
        "active_status",
        "created_at",
        "updated_at",
    ]

    list_filter = [
        "active_status",
    ]

    search_fields = [
        "food_type",
    ]

    list_display = [
        "food_type",
        "food_type_pic",
        "active_status",
        "created_at",
    ]

    actions = [make_active, make_deactive]

    list_per_page = 10
    # list_display_links = None

    def has_delete_permission(self, request, obj=None):
        return True

    def has_add_permission(self, request, obj=None):
        return True

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_at = datetime.now()
        else:
            obj.updated_at = datetime.now()
        obj.save()


class VariantMasterAdmin(admin.ModelAdmin):
    # form = CountryMasterForm
    exclude = [
        # 'status',
        "active_status",
        "created_at",
        "updated_at",
    ]

    list_filter = [
        "active_status",
    ]

    search_fields = [
        "variant",
    ]

    list_display = [
        "variant",
        "Company",
        "active_status",
        "created_at",
    ]

    actions = [make_active, make_deactive]
    list_display_links = None
    list_per_page = 10

    def has_delete_permission(self, request, obj=None):
        return True

    def has_add_permission(self, request, obj=None):
        return False

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_at = datetime.now()
        else:
            obj.updated_at = datetime.now()
        obj.save()


class AddonDetailsMasterAdmin(admin.ModelAdmin):
    # form = CountryMasterForm
    exclude = [
        "active_status",
        "created_at",
        "updated_at",
    ]

    list_filter = [
        "active_status",
    ]

    search_fields = [
        "addon_gr_name",
    ]

    list_display = [
        "addon_gr_name",
        "min_addons",
        "max_addons",
        "active_status",
        "created_at",
    ]

    actions = [make_active, make_deactive, addon_settings]

    # readonly_fields = [
    #     "active_status",
    #     "addon_gr_name",
    #     "min_addons",
    #     "max_addons",
    # ]
    # list_display_links = None
    list_per_page = 10

    def has_delete_permission(self, request, obj=None):
        return True

    def has_add_permission(self, request, obj=None):
        return False

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_at = datetime.now()
        else:
            obj.updated_at = datetime.now()
        obj.save()


class AddonsMasterAdmin(admin.ModelAdmin):
    # form = CountryMasterForm
    exclude = [
        # 'status',
        "created_at",
        "updated_at",
    ]

    list_filter = [ "active_status", "created_at"]

    search_fields = [
        "name",
    ]

    list_display = [
        "name",
        "addon_amount",
        "active_status",
        "created_at",
    ]

    actions = [make_active, make_deactive]

    # readonly_fields = [
    #     "name",
    #     "addon_amount",
    #     "active_status",
    # ]
    # list_display_links = None
    list_per_page = 10

    def has_delete_permission(self, request, obj=None):
        return True

    def has_add_permission(self, request, obj=None):
        return False

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_at = datetime.now()
        else:
            obj.updated_at = datetime.now()
        obj.save()


class ProductMasterAdmin(admin.ModelAdmin):
    # form = CountryMasterForm
    exclude = [
        # 'status',
        "active_status",
        "created_at",
        "updated_at",
    ]

    list_filter = ["active_status", "created_at", "updated_at", "Company__company_name"]

    search_fields = [
        "product_name",
    ]

    list_display = [
        "product_categorys",
        "product_subcategorys",
        "product_name",
        "image",
        "food_type",
        "priority",
        "active_status",
        "created_at",
    ]

    actions = [export_xls, make_active, make_deactive]
    # list_display_links = None
    list_per_page = 10

    def has_delete_permission(self, request, obj=None):
        return True

    def has_add_permission(self, request, obj=None):
        return False

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_at = datetime.now()
        else:
            obj.updated_at = datetime.now()
        obj.save()


class TagAdmin(admin.ModelAdmin):
    exclude = [
        "active_status",
        "created_at",
        "updated_at",
    ]

    list_filter = [
        "active_status",
        "created_at",
        "updated_at",
    ]

    search_fields = [
        "tag_name",
    ]

    list_display = [
        "tag_name",
        "company",
        "active_status",
        "created_at",
    ]

    actions = [make_active, make_deactive]
    list_display_links = None
    list_per_page = 10

    def has_delete_permission(self, request, obj=None):
        return True

    def has_add_permission(self, request, obj=None):
        return True

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_at = datetime.now()
        else:
            obj.updated_at = datetime.now()
        obj.save()


admin.site.register(ProductCategory, CategoryMasterAdmin)
admin.site.register(ProductsubCategory, SubCategoryMasterAdmin)
admin.site.register(Variant, VariantMasterAdmin)
admin.site.register(FoodType, FoodTypeMasterAdmin)
admin.site.register(AddonDetails, AddonDetailsMasterAdmin)
admin.site.register(Addons, AddonsMasterAdmin)
admin.site.register(Product, ProductMasterAdmin)
admin.site.register(Tag, TagAdmin)
