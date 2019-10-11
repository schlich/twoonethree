import re, os, io, csv, string
from django.core.management.base import BaseCommand
from tqdm import tqdm
from datetime import datetime
from mec.models import Committee, Contribution, Contributor, Company, Address, Individual



class Command(BaseCommand):

	def add_arguments(self,parser):
		parser.add_argument('files', nargs="*", type=str)
		parser.add_argument('--start_10k', dest="start_tenk", action='store_true')

	help = 'Import MEC CSV files to database'

	def handle(self, *args, **options):

		def csv_to_db(csv_path):
			csv_data = open(csv_path)
			csv_iterable = csv.DictReader(csv_data)

			c_iter = 0
			for row in tqdm(csv_iterable, total=len(io.open(csv_path).readlines())):
				c_iter += 1
				if (options["start_tenk"]):
					if(c_iter< 50000):
						continue
				translator = str.maketrans('','', string.punctuation)
				to_mec_id = row[" MECID"].strip()
				to_committee_name = row["Committee Name"].title().translate(translator).strip()
				fr_comm_name = row["Committee"].title().translate(translator).strip()
				fr_corp_name = row["Company"].title().translate(translator).strip()
				fr_first_name = row["First Name"].title().strip().translate(translator)
				fr_last_name = row["Last Name"].title().strip().translate(translator)
				fr_addr_one = row["Address 1"].title().strip().translate(translator)
				fr_addr_two = row["Address 2"].title().strip().translate(translator)
				fr_city = row["City"].title().strip().translate(translator)
				fr_state = row["State"].upper().strip()
				fr_zip = row["Zip"].strip()
				fr_employer = row["Employer"].title().strip().translate(translator)
				fr_occupation = row["Occupation"].title().strip().translate(translator)
				t_id = row["CD1_A ID"] + '_A'
				t_date = datetime.strptime(row["Date"].split(" ")[0], "%m/%d/%Y").date()
				t_amount = row["Amount"]
				t_con_type = row["Contribution Type"]
				t_report = row["Report"]

				addr_obj, addr_created = Address.objects.get_or_create(
					address1=fr_addr_one,
					address2=fr_addr_two,
					city=fr_city,
					state=fr_state,
					zip=fr_zip,

				)

				to_obj, to_created = Committee.objects.update_or_create(
					name=to_committee_name,
					defaults={
						"MECID": to_mec_id,
					}
				)

				if fr_comm_name:
					fr_comm, fr_comm_created = Committee.objects.get_or_create(
						name=fr_comm_name,
					)
					fr_obj, fr_created = Contributor.objects.get_or_create(
						committee = fr_comm,
						defaults = {
							'address': addr_obj,
						}
					)
				elif fr_first_name or fr_last_name:
					ind_obj, ind_created = Individual.objects.get_or_create(
						first_name = fr_first_name,
						last_name = fr_last_name,
						defaults = {
							"occupation": fr_occupation,
							"employer": fr_employer,
						}
					)

					fr_obj, fr_created = Contributor.objects.get_or_create(
						individual = ind_obj,
						defaults = {
							'address': addr_obj,
						}
					)
				elif fr_corp_name:
					fr_corp, fr_com_created = Company.objects.update_or_create(
						name = fr_corp_name,
					)
					fr_obj, fr_created = Contributor.objects.get_or_create(
						company = fr_corp,
						defaults = {
							'address': addr_obj,
						}
					)

				t_str = u"{} to {} in amount {}.".format(fr_obj, to_obj, t_amount)

				tqdm.write(t_str)

				contribution, t_created =  Contribution.objects.get_or_create(
                    id = t_id,
					recipient = to_obj,
                    contributor = fr_obj,
                    date = t_date,
                    amount = t_amount,
                    donation_type = t_con_type,
                    report = t_report,
                )

				tqdm.write("Created." if t_created else "Already exists.")

		target_directory = os.path.join(os.path.expanduser("~"), 'mec')

		for file in os.listdir(target_directory):
			if file.endswith(".csv"):
				print("Starting {}.".format(file))
				csv_to_db(os.path.join(target_directory, file))
				print("Finished {}.".format(file))