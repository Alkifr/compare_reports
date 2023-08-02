class SqlQueries():


	def get_kupol_log_from_test():
		return f'''
		select *
from [DBA].ISAPMessageOrder io 
where CAST(MessageTime as date) >= '2022-09-01'
		'''

	def get_queries_so_from_kupol():
		return f'''
			select 
t_all.name_store,
--t_all.id_,
cast(t_all.elt_bn as nvarchar) as elt_bn,
cast(t_all.elt_id as nvarchar) as elt_id,
t_all.pn,
t_all.sn,
sum(t_all.qty_released) as qty_released,
sum(t_all.qty_restocked) as qty_restocked,
t_all.symbolint,
cast(t_all.idsof_ as nvarchar) as idsof_,
t_all.transactiontype as sof_type,
cast(t_all.sofdate_ as date) as SOFdate_,
t_all.registrationnumber as registrationnumber,
t_all.IDPROPERTY,
[DBA].MJSS.MJSSNumber,
[DBA].MJSSType.MJSSType,
[DBA].StoreBalanceType.BalanceCode,
pns.Description, pns.KeyWordTranslation, 
cast(pns.GUID1C as nvarchar) as GUID1C, 
errors.*,
t_all.idcustomer_,
t_all.idum_,
case 
	when t_all.IDPROPERTY != '560' then 'Собственник не НордСтар!'
	when LENGTH(TRIM(t_all.ELT_ID))>0 /*and t_all.transactiontype != 'UTILIZATION'*/ then 'Инструмент'
	--when t_all.ELT_ID is not null and t_all.transactiontype != 'REPAIR' then 'Инструмент'
	when t_all.transactiontype != 'PRODUCTION' or t_all.transactiontype is not null then 'Тип SO не входит к отправке'
	when [DBA].StoreBalanceType.BalanceCode is null then 'Тип баланса не определен!'
	when [DBA].StoreBalanceType.BalanceCode != 'C' then 'Забаланс'
	else 'К отправке в 1С'
end as statusSO,
case 
	when errors.KSIPResponse = '200' then 'Отправлен в 1С'
	when errors.KSIPResponse = '-200' then 'Ошибка отправки'
	when errors.KSIPResponse is null then 'Не отправлен'
	else null
end as StatusLog
from(
select 
number_store,
name_store,
IDMJSS,
t.id_,
t.ELT_BN,
t.ELT_ID,
QTY_Released,
QTY_Restocked,
t.IDSOF_,
t.SOFdate_,
registrationnumber,
IDPROPERTY,
Symbolint,
pn,
sn,
TransactionType,
IDBalanceType,
t.IDCustomer_,
t.Idum_
from(
select 
SV_DME_NS2_StoreOutItems.*,
SV_DME_NS2_StoreOut.*,
SV_DME_NS2_Store.PN,
SV_DME_NS2_Store.SN,
SV_DME_NS2_Store.ELT_ID,
SV_DME_NS2_Store.IDBalanceType,
106 as number_store,
'SV_DME_NS2' as name_store,
[DBA].SV_DME_NS2_StoreOutItems.id as id_,
[DBA].SV_DME_NS2_StoreOutItems.IDSOF as IDSOF_,
[DBA].SV_DME_NS2_StoreOut.SOFdate as SOFdate_,
StoreOutTransactions.TransactionType,
[DBA].SV_DME_NS2_StoreOut.IDCustomer as IDCustomer_,
[DBA].SV_DME_NS2_Store.IDUM as IDum_,
bum.SymbolInt,
at2.RegistrationNumber
from [DBA].SV_DME_NS2_StoreOutItems
join [DBA].SV_DME_NS2_StoreOut on [DBA].SV_DME_NS2_StoreOut.ID = [DBA].SV_DME_NS2_StoreOutItems.IDSOF
left join [DBA].SOTransactionsCross on [DBA].SOTransactionsCross.IDStore = number_store and [DBA].SOTransactionsCross.IDSOF = [DBA].SV_DME_NS2_StoreOut.ID
left join [DBA].StoreOutTransactions on [DBA].StoreOutTransactions.ID = [DBA].SOTransactionsCross.IDStoreOutTransaction
left join [DBA].SV_DME_NS2_Store on [DBA].SV_DME_NS2_Store.ELT_BN = [DBA].SV_DME_NS2_StoreOutItems.ELT_BN and [DBA].SV_DME_NS2_Store.ID = [DBA].SV_DME_NS2_StoreOutItems.IDInStoreTable
left join [mma].BasUnMeas bum on bum.ID = SV_DME_NS2_Store.IDUM
left join [dba].ACRegType at2 on at2.ID = SV_DME_NS2_StoreOut.IDACReg
union
select
QR_DME_NS2_StoreOutItems.*,
QR_DME_NS2_StoreOut.*,
QR_DME_NS2_Store.PN,
QR_DME_NS2_Store.SN,
QR_DME_NS2_Store.ELT_ID,
QR_DME_NS2_Store.IDBalanceType,
116 as number_store,
'QR_DME_NS2' as name_store,
[DBA].QR_DME_NS2_StoreOutItems.id as id_,
[DBA].QR_DME_NS2_StoreOutItems.IDSOF as IDSOF_,
[DBA].QR_DME_NS2_StoreOut.SOFdate as SOFdate_,
StoreOutTransactions.TransactionType,
[DBA].QR_DME_NS2_StoreOut.IDCustomer as IDCustomer_,
[DBA].QR_DME_NS2_Store.IDUM as IDum_,
bum.SymbolInt,
at2.RegistrationNumber
from [DBA].QR_DME_NS2_StoreOutItems
join [DBA].QR_DME_NS2_StoreOut on [DBA].QR_DME_NS2_StoreOut.ID = [DBA].QR_DME_NS2_StoreOutItems.IDSOF
left join [DBA].SOTransactionsCross on [DBA].SOTransactionsCross.IDStore = number_store and [DBA].SOTransactionsCross.IDSOF = [DBA].QR_DME_NS2_StoreOut.ID
left join [DBA].StoreOutTransactions on [DBA].StoreOutTransactions.ID = [DBA].SOTransactionsCross.IDStoreOutTransaction
left join [DBA].QR_DME_NS2_Store on [DBA].QR_DME_NS2_Store.ELT_BN = [DBA].QR_DME_NS2_StoreOutItems.ELT_BN and [DBA].QR_DME_NS2_Store.ID = [DBA].QR_DME_NS2_StoreOutItems.IDInStoreTable 
left join [mma].BasUnMeas bum on bum.ID = QR_DME_NS2_Store.IDUM
left join [dba].ACRegType at2 on at2.ID = QR_DME_NS2_StoreOut.IDACReg
union
select
QR_KJA_NS_StoreOutItems.*,
QR_KJA_NS_StoreOut.*,
QR_KJA_NS_Store.PN,
QR_KJA_NS_Store.SN,
QR_KJA_NS_Store.ELT_ID,
QR_KJA_NS_Store.IDBalanceType,
117 as number_store,
'QR_KJA_NS' as name_store,
[DBA].QR_KJA_NS_StoreOutItems.id as id_,
[DBA].QR_KJA_NS_StoreOutItems.IDSOF as IDSOF_,
[DBA].QR_KJA_NS_StoreOut.SOFdate as SOFdate_,
StoreOutTransactions.TransactionType,
[DBA].QR_KJA_NS_StoreOut.IDCustomer as IDCustomer_,
[DBA].QR_KJA_NS_Store.IDUM as IDum_,
bum.SymbolInt,
at2.RegistrationNumber
from [DBA].QR_KJA_NS_StoreOutItems
join [DBA].QR_KJA_NS_StoreOut on [DBA].QR_KJA_NS_StoreOut.ID = [DBA].QR_KJA_NS_StoreOutItems.IDSOF
left join [DBA].SOTransactionsCross on [DBA].SOTransactionsCross.IDStore = number_store and [DBA].SOTransactionsCross.IDSOF = [DBA].QR_KJA_NS_StoreOut.ID
left join [DBA].StoreOutTransactions on [DBA].StoreOutTransactions.ID = [DBA].SOTransactionsCross.IDStoreOutTransaction
left join [DBA].QR_KJA_NS_Store on [DBA].QR_KJA_NS_Store.ELT_BN = [DBA].QR_KJA_NS_StoreOutItems.ELT_BN and [DBA].QR_KJA_NS_Store.ID = [DBA].QR_KJA_NS_StoreOutItems.IDInStoreTable
left join [mma].BasUnMeas bum on bum.ID = QR_KJA_NS_Store.IDUM
left join [dba].ACRegType at2 on at2.ID = QR_KJA_NS_StoreOut.IDACReg
union
select 
QR_NSK_NS_StoreOutItems.*,
QR_NSK_NS_StoreOut.*,
QR_NSK_NS_Store.PN,
QR_NSK_NS_Store.SN,
QR_NSK_NS_Store.ELT_ID,
QR_NSK_NS_Store.IDBalanceType,
118 as number_store,
'QR_NSK_NS' as name_store,
[DBA].QR_NSK_NS_StoreOutItems.id as id_,
[DBA].QR_NSK_NS_StoreOutItems.IDSOF as IDSOF_,
[DBA].QR_NSK_NS_StoreOut.SOFdate as SOFdate_,
StoreOutTransactions.TransactionType,
[DBA].QR_NSK_NS_StoreOut.IDCustomer as IDCustomer_,
[DBA].QR_NSK_NS_Store.IDUM as IDum_,
bum.SymbolInt,
at2.RegistrationNumber
from [DBA].QR_NSK_NS_StoreOutItems
join [DBA].QR_NSK_NS_StoreOut on [DBA].QR_NSK_NS_StoreOut.ID = [DBA].QR_NSK_NS_StoreOutItems.IDSOF
left join [DBA].SOTransactionsCross on [DBA].SOTransactionsCross.IDStore = number_store and [DBA].SOTransactionsCross.IDSOF = [DBA].QR_NSK_NS_StoreOut.ID
left join [DBA].StoreOutTransactions on [DBA].StoreOutTransactions.ID = [DBA].SOTransactionsCross.IDStoreOutTransaction
left join [DBA].QR_NSK_NS_Store on [DBA].QR_NSK_NS_Store.ELT_BN = [DBA].QR_NSK_NS_StoreOutItems.ELT_BN and [DBA].QR_NSK_NS_Store.ID = [DBA].QR_NSK_NS_StoreOutItems.IDInStoreTable
left join [mma].BasUnMeas bum on bum.ID = QR_NSK_NS_Store.IDUM
left join [dba].ACRegType at2 on at2.ID = QR_NSK_NS_StoreOut.IDACReg
union
select 
QR_ZIA_NS_StoreOutItems.*,
QR_ZIA_NS_StoreOut.*,
QR_ZIA_NS_Store.PN,
QR_ZIA_NS_Store.SN,
QR_ZIA_NS_Store.ELT_ID,
QR_ZIA_NS_Store.IDBalanceType,
131 as number_store,
'QR_ZIA_NS' as name_store,
[DBA].QR_ZIA_NS_StoreOutItems.id as id_,
[DBA].QR_ZIA_NS_StoreOutItems.IDSOF as IDSOF_,
[DBA].QR_ZIA_NS_StoreOut.SOFdate as SOFdate_,
StoreOutTransactions.TransactionType,
[DBA].QR_ZIA_NS_StoreOut.IDCustomer as IDCustomer_,
[DBA].QR_ZIA_NS_Store.IDUM as IDum_,
bum.SymbolInt,
at2.RegistrationNumber
from [DBA].QR_ZIA_NS_StoreOutItems
join [DBA].QR_ZIA_NS_StoreOut on [DBA].QR_ZIA_NS_StoreOut.ID = [DBA].QR_ZIA_NS_StoreOutItems.IDSOF
left join [DBA].SOTransactionsCross on [DBA].SOTransactionsCross.IDStore = number_store and [DBA].SOTransactionsCross.IDSOF = [DBA].QR_ZIA_NS_StoreOut.ID
left join [DBA].StoreOutTransactions on [DBA].StoreOutTransactions.ID = [DBA].SOTransactionsCross.IDStoreOutTransaction
left join [DBA].QR_ZIA_NS_Store on [DBA].QR_ZIA_NS_Store.ELT_BN = [DBA].QR_ZIA_NS_StoreOutItems.ELT_BN and [DBA].QR_ZIA_NS_Store.ID = [DBA].QR_ZIA_NS_StoreOutItems.IDInStoreTable
left join [mma].BasUnMeas bum on bum.ID = QR_ZIA_NS_Store.IDUM
left join [dba].ACRegType at2 on at2.ID = QR_ZIA_NS_StoreOut.IDACReg
union
select
SV_ABA_NS_StoreOutItems.*,
SV_ABA_NS_StoreOut.*,
SV_ABA_NS_Store.PN,
SV_ABA_NS_Store.SN,
SV_ABA_NS_Store.ELT_ID,
SV_ABA_NS_Store.IDBalanceType,
121 as number_store,
'SV_ABA_NS' as name_store,
[DBA].SV_ABA_NS_StoreOutItems.id as id_,
[DBA].SV_ABA_NS_StoreOutItems.IDSOF as IDSOF_,
[DBA].SV_ABA_NS_StoreOut.SOFdate as SOFdate_,
StoreOutTransactions.TransactionType,
[DBA].SV_ABA_NS_StoreOut.IDCustomer as IDCustomer_,
[DBA].SV_ABA_NS_Store.IDUM as IDum_,
bum.SymbolInt,
at2.RegistrationNumber
from [DBA].SV_ABA_NS_StoreOutItems
join [DBA].SV_ABA_NS_StoreOut on [DBA].SV_ABA_NS_StoreOut.ID = [DBA].SV_ABA_NS_StoreOutItems.IDSOF
left join [DBA].SOTransactionsCross on [DBA].SOTransactionsCross.IDStore = number_store and [DBA].SOTransactionsCross.IDSOF = [DBA].SV_ABA_NS_StoreOut.ID
left join [DBA].StoreOutTransactions on [DBA].StoreOutTransactions.ID = [DBA].SOTransactionsCross.IDStoreOutTransaction
left join [DBA].SV_ABA_NS_Store on [DBA].SV_ABA_NS_Store.ELT_BN = [DBA].SV_ABA_NS_StoreOutItems.ELT_BN and [DBA].SV_ABA_NS_Store.ID = [DBA].SV_ABA_NS_StoreOutItems.IDInStoreTable
left join [mma].BasUnMeas bum on bum.ID = SV_ABA_NS_Store.IDUM
left join [dba].ACRegType at2 on at2.ID = SV_ABA_NS_StoreOut.IDACReg
union
select 
SV_ABROAD_CHECK_NS_StoreOutItems.*,
SV_ABROAD_CHECK_NS_StoreOut.*,
SV_ABROAD_CHECK_NS_Store.PN,
SV_ABROAD_CHECK_NS_Store.SN,
SV_ABROAD_CHECK_NS_Store.ELT_ID,
SV_ABROAD_CHECK_NS_Store.IDBalanceType,
111 as number_store,
'SV_ABROAD_CHECK_NS' as name_store,
[DBA].SV_ABROAD_CHECK_NS_StoreOutItems.id as id_,
[DBA].SV_ABROAD_CHECK_NS_StoreOutItems.IDSOF as IDSOF_,
[DBA].SV_ABROAD_CHECK_NS_StoreOut.SOFdate as SOFdate_,
StoreOutTransactions.TransactionType,
[DBA].SV_ABROAD_CHECK_NS_StoreOut.IDCustomer as IDCustomer_,
[DBA].SV_ABROAD_CHECK_NS_Store.IDUM as IDum_,
bum.SymbolInt,
at2.RegistrationNumber
from [DBA].SV_ABROAD_CHECK_NS_StoreOutItems
join [DBA].SV_ABROAD_CHECK_NS_StoreOut on [DBA].SV_ABROAD_CHECK_NS_StoreOut.ID = [DBA].SV_ABROAD_CHECK_NS_StoreOutItems.IDSOF
left join [DBA].SOTransactionsCross on [DBA].SOTransactionsCross.IDStore = number_store and [DBA].SOTransactionsCross.IDSOF = [DBA].SV_ABROAD_CHECK_NS_StoreOut.ID
left join [DBA].StoreOutTransactions on [DBA].StoreOutTransactions.ID = [DBA].SOTransactionsCross.IDStoreOutTransaction
left join [DBA].SV_ABROAD_CHECK_NS_Store on [DBA].SV_ABROAD_CHECK_NS_Store.ELT_BN = [DBA].SV_ABROAD_CHECK_NS_StoreOutItems.ELT_BN and [DBA].SV_ABROAD_CHECK_NS_Store.ID = [DBA].SV_ABROAD_CHECK_NS_StoreOutItems.IDInStoreTable 
left join [mma].BasUnMeas bum on bum.ID = SV_ABROAD_CHECK_NS_Store.IDUM
left join [dba].ACRegType at2 on at2.ID = SV_ABROAD_CHECK_NS_StoreOut.IDACReg
union
select
SV_DME_UTG_StoreOutItems.*,
SV_DME_UTG_StoreOut.*,
SV_DME_UTG_Store.PN,
SV_DME_UTG_Store.SN,
SV_DME_UTG_Store.ELT_ID,
SV_DME_UTG_Store.IDBalanceType,
102 as number_store,
'SV_DME_UTG' as name_store,
[DBA].SV_DME_UTG_StoreOutItems.id as id_,
[DBA].SV_DME_UTG_StoreOutItems.IDSOF as IDSOF_,
[DBA].SV_DME_UTG_StoreOut.SOFdate as SOFdate_,
StoreOutTransactions.TransactionType,
[DBA].SV_DME_UTG_StoreOut.IDCustomer as IDCustomer_,
[DBA].SV_DME_UTG_Store.IDUM as IDum_,
bum.SymbolInt,
at2.RegistrationNumber
from [DBA].SV_DME_UTG_StoreOutItems
join [DBA].SV_DME_UTG_StoreOut on [DBA].SV_DME_UTG_StoreOut.ID = [DBA].SV_DME_UTG_StoreOutItems.IDSOF
left join [DBA].SOTransactionsCross on [DBA].SOTransactionsCross.IDStore = number_store and [DBA].SOTransactionsCross.IDSOF = [DBA].SV_DME_UTG_StoreOut.ID
left join [DBA].StoreOutTransactions on [DBA].StoreOutTransactions.ID = [DBA].SOTransactionsCross.IDStoreOutTransaction
left join [DBA].SV_DME_UTG_Store on [DBA].SV_DME_UTG_Store.ELT_BN = [DBA].SV_DME_UTG_StoreOutItems.ELT_BN and [DBA].SV_DME_UTG_Store.ID = [DBA].SV_DME_UTG_StoreOutItems.IDInStoreTable
left join [mma].BasUnMeas bum on bum.ID = SV_DME_UTG_Store.IDUM
left join [dba].ACRegType at2 on at2.ID = SV_DME_UTG_StoreOut.IDACReg
union
select 
SV_KJA_KA_StoreOutItems.*,
SV_KJA_KA_StoreOut.*,
SV_KJA_KA_Store.PN,
SV_KJA_KA_Store.SN,
SV_KJA_KA_Store.ELT_ID,
SV_KJA_KA_Store.IDBalanceType,
124 as number_store,
'SV_KJA_KA' as name_store,
[DBA].SV_KJA_KA_StoreOutItems.id as id_,
[DBA].SV_KJA_KA_StoreOutItems.IDSOF as IDSOF_,
[DBA].SV_KJA_KA_StoreOut.SOFdate as SOFdate_,
StoreOutTransactions.TransactionType,
[DBA].SV_KJA_KA_StoreOut.IDCustomer as IDCustomer_,
[DBA].SV_KJA_KA_Store.IDUM as IDum_,
bum.SymbolInt,
at2.RegistrationNumber
from [DBA].SV_KJA_KA_StoreOutItems
join [DBA].SV_KJA_KA_StoreOut on [DBA].SV_KJA_KA_StoreOut.ID = [DBA].SV_KJA_KA_StoreOutItems.IDSOF
left join [DBA].SOTransactionsCross on [DBA].SOTransactionsCross.IDStore = number_store and [DBA].SOTransactionsCross.IDSOF = [DBA].SV_KJA_KA_StoreOut.ID
left join [DBA].StoreOutTransactions on [DBA].StoreOutTransactions.ID = [DBA].SOTransactionsCross.IDStoreOutTransaction
left join [DBA].SV_KJA_KA_Store on [DBA].SV_KJA_KA_Store.ELT_BN = [DBA].SV_KJA_KA_StoreOutItems.ELT_BN and [DBA].SV_KJA_KA_Store.ID = [DBA].SV_KJA_KA_StoreOutItems.IDInStoreTable
left join [mma].BasUnMeas bum on bum.ID = SV_KJA_KA_Store.IDUM
left join [dba].ACRegType at2 on at2.ID = SV_KJA_KA_StoreOut.IDACReg
union
select
SV_KJA_NS_StoreOutItems.*,
SV_KJA_NS_StoreOut.*,
SV_KJA_NS_Store.PN,
SV_KJA_NS_Store.SN,
SV_KJA_NS_Store.ELT_ID,
SV_KJA_NS_Store.IDBalanceType,
104 as number_store,
'SV_KJA_NS' as name_store,
[DBA].SV_KJA_NS_StoreOutItems.id as id_,
[DBA].SV_KJA_NS_StoreOutItems.IDSOF as IDSOF_,
[DBA].SV_KJA_NS_StoreOut.SOFdate as SOFdate_,
StoreOutTransactions.TransactionType,
[DBA].SV_KJA_NS_StoreOut.IDCustomer as IDCustomer_,
[DBA].SV_KJA_NS_Store.IDUM as IDum_,
bum.SymbolInt,
at2.RegistrationNumber
from [DBA].SV_KJA_NS_StoreOutItems
join [DBA].SV_KJA_NS_StoreOut on [DBA].SV_KJA_NS_StoreOut.ID = [DBA].SV_KJA_NS_StoreOutItems.IDSOF
left join [DBA].SOTransactionsCross on [DBA].SOTransactionsCross.IDStore = number_store and [DBA].SOTransactionsCross.IDSOF = [DBA].SV_KJA_NS_StoreOut.ID
left join [DBA].StoreOutTransactions on [DBA].StoreOutTransactions.ID = [DBA].SOTransactionsCross.IDStoreOutTransaction
left join [DBA].SV_KJA_NS_Store on [DBA].SV_KJA_NS_Store.ELT_BN = [DBA].SV_KJA_NS_StoreOutItems.ELT_BN and [DBA].SV_KJA_NS_Store.ID = [DBA].SV_KJA_NS_StoreOutItems.IDInStoreTable
left join [mma].BasUnMeas bum on bum.ID = SV_KJA_NS_Store.IDUM
left join [dba].ACRegType at2 on at2.ID = SV_KJA_NS_StoreOut.IDACReg
union
select 
SV_NSK_NS2_StoreOutItems.*,
SV_NSK_NS2_StoreOut.*,
SV_NSK_NS2_Store.PN,
SV_NSK_NS2_Store.SN,
SV_NSK_NS2_Store.ELT_ID,
SV_NSK_NS2_Store.IDBalanceType,
108 as number_store,
'SV_NSK_NS2' as name_store,
[DBA].SV_NSK_NS2_StoreOutItems.id as id_,
[DBA].SV_NSK_NS2_StoreOutItems.IDSOF as IDSOF_,
[DBA].SV_NSK_NS2_StoreOut.SOFdate as SOFdate_,
StoreOutTransactions.TransactionType,
[DBA].SV_NSK_NS2_StoreOut.IDCustomer as IDCustomer_,
[DBA].SV_NSK_NS2_Store.IDUM as IDum_,
bum.SymbolInt,
at2.RegistrationNumber
from [DBA].SV_NSK_NS2_StoreOutItems
join [DBA].SV_NSK_NS2_StoreOut on [DBA].SV_NSK_NS2_StoreOut.ID = [DBA].SV_NSK_NS2_StoreOutItems.IDSOF
left join [DBA].SOTransactionsCross on [DBA].SOTransactionsCross.IDStore = number_store and [DBA].SOTransactionsCross.IDSOF = [DBA].SV_NSK_NS2_StoreOut.ID
left join [DBA].StoreOutTransactions on [DBA].StoreOutTransactions.ID = [DBA].SOTransactionsCross.IDStoreOutTransaction
left join [DBA].SV_NSK_NS2_Store on [DBA].SV_NSK_NS2_Store.ELT_BN = [DBA].SV_NSK_NS2_StoreOutItems.ELT_BN and [DBA].SV_NSK_NS2_Store.ID = [DBA].SV_NSK_NS2_StoreOutItems.IDInStoreTable
left join [mma].BasUnMeas bum on bum.ID = SV_NSK_NS2_Store.IDUM
left join [dba].ACRegType at2 on at2.ID = SV_NSK_NS2_StoreOut.IDACReg
union
select 
SV_NUX_NS_StoreOutItems.*,
SV_NUX_NS_StoreOut.*,
SV_NUX_NS_Store.PN,
SV_NUX_NS_Store.SN,
SV_NUX_NS_Store.ELT_ID,
SV_NUX_NS_Store.IDBalanceType,
100 as number_store,
'SV_NUX_NS' as name_store,
[DBA].SV_NUX_NS_StoreOutItems.id as id_,
[DBA].SV_NUX_NS_StoreOutItems.IDSOF as IDSOF_,
[DBA].SV_NUX_NS_StoreOut.SOFdate as SOFdate_,
StoreOutTransactions.TransactionType,
[DBA].SV_NUX_NS_StoreOut.IDCustomer as IDCustomer_,
[DBA].SV_NUX_NS_Store.IDUM as IDum_,
bum.SymbolInt,
at2.RegistrationNumber
from [DBA].SV_NUX_NS_StoreOutItems
join [DBA].SV_NUX_NS_StoreOut on [DBA].SV_NUX_NS_StoreOut.ID = [DBA].SV_NUX_NS_StoreOutItems.IDSOF
left join [DBA].SOTransactionsCross on [DBA].SOTransactionsCross.IDStore = number_store and [DBA].SOTransactionsCross.IDSOF = [DBA].SV_NUX_NS_StoreOut.ID
left join [DBA].StoreOutTransactions on [DBA].StoreOutTransactions.ID = [DBA].SOTransactionsCross.IDStoreOutTransaction
left join [DBA].SV_NUX_NS_Store on [DBA].SV_NUX_NS_Store.ELT_BN = [DBA].SV_NUX_NS_StoreOutItems.ELT_BN and [DBA].SV_NUX_NS_Store.ID = [DBA].SV_NUX_NS_StoreOutItems.IDInStoreTable
left join [mma].BasUnMeas bum on bum.ID = SV_NUX_NS_Store.IDUM
left join [dba].ACRegType at2 on at2.ID = SV_NUX_NS_StoreOut.IDACReg
union
select 
SV_SGC_NS_StoreOutItems.*,
SV_SGC_NS_StoreOut.*,
SV_SGC_NS_Store.PN,
SV_SGC_NS_Store.SN,
SV_SGC_NS_Store.ELT_ID,
SV_SGC_NS_Store.IDBalanceType,
93 as number_store,
'SV_SGC_NS' as name_store,
[DBA].SV_SGC_NS_StoreOutItems.id as id_,
[DBA].SV_SGC_NS_StoreOutItems.IDSOF as IDSOF_,
[DBA].SV_SGC_NS_StoreOut.SOFdate as SOFdate_,
StoreOutTransactions.TransactionType,
[DBA].SV_SGC_NS_StoreOut.IDCustomer as IDCustomer_,
[DBA].SV_SGC_NS_Store.IDUM as IDum_,
bum.SymbolInt,
at2.RegistrationNumber
from [DBA].SV_SGC_NS_StoreOutItems
join [DBA].SV_SGC_NS_StoreOut on [DBA].SV_SGC_NS_StoreOut.ID = [DBA].SV_SGC_NS_StoreOutItems.IDSOF
left join [DBA].SOTransactionsCross on [DBA].SOTransactionsCross.IDStore = number_store and [DBA].SOTransactionsCross.IDSOF = [DBA].SV_SGC_NS_StoreOut.ID
left join [DBA].StoreOutTransactions on [DBA].StoreOutTransactions.ID = [DBA].SOTransactionsCross.IDStoreOutTransaction
left join [DBA].SV_SGC_NS_Store on [DBA].SV_SGC_NS_Store.ELT_BN = [DBA].SV_SGC_NS_StoreOutItems.ELT_BN and [DBA].SV_SGC_NS_Store.ID = [DBA].SV_SGC_NS_StoreOutItems.IDInStoreTable
left join [mma].BasUnMeas bum on bum.ID = SV_SGC_NS_Store.IDUM
left join [dba].ACRegType at2 on at2.ID = SV_SGC_NS_StoreOut.IDACReg
union
select 
SV_VKO_UTG_NS_StoreOutItems.*,
SV_VKO_UTG_NS_StoreOut.*,
SV_VKO_UTG_NS_Store.PN,
SV_VKO_UTG_NS_Store.SN,
SV_VKO_UTG_NS_Store.ELT_ID,
SV_VKO_UTG_NS_Store.IDBalanceType,
110 as number_store,
'SV_VKO_UTG_NS' as name_store,
[DBA].SV_VKO_UTG_NS_StoreOutItems.id as id_,
[DBA].SV_VKO_UTG_NS_StoreOutItems.IDSOF as IDSOF_,
[DBA].SV_VKO_UTG_NS_StoreOut.SOFdate as SOFdate_,
StoreOutTransactions.TransactionType,
[DBA].SV_VKO_UTG_NS_StoreOut.IDCustomer as IDCustomer_,
[DBA].SV_VKO_UTG_NS_Store.IDUM as IDum_,
bum.SymbolInt,
at2.RegistrationNumber
from [DBA].SV_VKO_UTG_NS_StoreOutItems
join [DBA].SV_VKO_UTG_NS_StoreOut on [DBA].SV_VKO_UTG_NS_StoreOut.ID = [DBA].SV_VKO_UTG_NS_StoreOutItems.IDSOF
left join [DBA].SOTransactionsCross on [DBA].SOTransactionsCross.IDStore = number_store and [DBA].SOTransactionsCross.IDSOF = [DBA].SV_VKO_UTG_NS_StoreOut.ID
left join [DBA].StoreOutTransactions on [DBA].StoreOutTransactions.ID = [DBA].SOTransactionsCross.IDStoreOutTransaction
left join [DBA].SV_VKO_UTG_NS_Store on [DBA].SV_VKO_UTG_NS_Store.ELT_BN = [DBA].SV_VKO_UTG_NS_StoreOutItems.ELT_BN and [DBA].SV_VKO_UTG_NS_Store.ID = [DBA].SV_VKO_UTG_NS_StoreOutItems.IDInStoreTable
left join [mma].BasUnMeas bum on bum.ID = SV_VKO_UTG_NS_Store.IDUM
left join [dba].ACRegType at2 on at2.ID = SV_VKO_UTG_NS_StoreOut.IDACReg
union
select 
SV_ZIA_NS_StoreOutItems.*,
SV_ZIA_NS_StoreOut.*,
SV_ZIA_NS_Store.PN,
SV_ZIA_NS_Store.SN,
SV_ZIA_NS_Store.ELT_ID,
SV_ZIA_NS_Store.IDBalanceType,
129 as number_store,
'SV_ZIA_NS' as name_store,
[DBA].SV_ZIA_NS_StoreOutItems.id as id_,
[DBA].SV_ZIA_NS_StoreOutItems.IDSOF as IDSOF_,
[DBA].SV_ZIA_NS_StoreOut.SOFdate as SOFdate_,
StoreOutTransactions.TransactionType,
[DBA].SV_ZIA_NS_StoreOut.IDCustomer as IDCustomer_,
[DBA].SV_ZIA_NS_Store.IDUM as IDum_,
bum.SymbolInt,
at2.RegistrationNumber
from [DBA].SV_ZIA_NS_StoreOutItems
join [DBA].SV_ZIA_NS_StoreOut on [DBA].SV_ZIA_NS_StoreOut.ID = [DBA].SV_ZIA_NS_StoreOutItems.IDSOF
left join [DBA].SOTransactionsCross on [DBA].SOTransactionsCross.IDStore = number_store and [DBA].SOTransactionsCross.IDSOF = [DBA].SV_ZIA_NS_StoreOut.ID
left join [DBA].StoreOutTransactions on [DBA].StoreOutTransactions.ID = [DBA].SOTransactionsCross.IDStoreOutTransaction
left join [DBA].SV_ZIA_NS_Store on [DBA].SV_ZIA_NS_Store.ELT_BN = [DBA].SV_ZIA_NS_StoreOutItems.ELT_BN and [DBA].SV_ZIA_NS_Store.ID = [DBA].SV_ZIA_NS_StoreOutItems.IDInStoreTable
left join [mma].BasUnMeas bum on bum.ID = SV_ZIA_NS_Store.IDUM
left join [dba].ACRegType at2 on at2.ID = SV_ZIA_NS_StoreOut.IDACReg
union
select 
SV_ZIA_UTG_NS_StoreOutItems.*,
SV_ZIA_UTG_NS_StoreOut.*,
SV_ZIA_UTG_NS_Store.PN,
SV_ZIA_UTG_NS_Store.SN,
SV_ZIA_UTG_NS_Store.ELT_ID,
SV_ZIA_UTG_NS_Store.IDBalanceType,
132 as number_store,
'SV_ZIA_UTG_NS' as name_store,
[DBA].SV_ZIA_UTG_NS_StoreOutItems.id as id_,
[DBA].SV_ZIA_UTG_NS_StoreOutItems.IDSOF as IDSOF_,
[DBA].SV_ZIA_UTG_NS_StoreOut.SOFdate as SOFdate_,
StoreOutTransactions.TransactionType,
[DBA].SV_ZIA_UTG_NS_StoreOut.IDCustomer as IDCustomer_,
[DBA].SV_ZIA_UTG_NS_Store.IDUM as IDum_,
bum.SymbolInt,
at2.RegistrationNumber
from [DBA].SV_ZIA_UTG_NS_StoreOutItems
join [DBA].SV_ZIA_UTG_NS_StoreOut on [DBA].SV_ZIA_UTG_NS_StoreOut.ID = [DBA].SV_ZIA_UTG_NS_StoreOutItems.IDSOF
left join [DBA].SOTransactionsCross on [DBA].SOTransactionsCross.IDStore = number_store and [DBA].SOTransactionsCross.IDSOF = [DBA].SV_ZIA_UTG_NS_StoreOut.ID
left join [DBA].StoreOutTransactions on [DBA].StoreOutTransactions.ID = [DBA].SOTransactionsCross.IDStoreOutTransaction
left join [DBA].SV_ZIA_UTG_NS_Store on [DBA].SV_ZIA_UTG_NS_Store.ELT_BN = [DBA].SV_ZIA_UTG_NS_StoreOutItems.ELT_BN and [DBA].SV_ZIA_UTG_NS_Store.ID = [DBA].SV_ZIA_UTG_NS_StoreOutItems.IDInStoreTable
left join [mma].BasUnMeas bum on bum.ID = SV_ZIA_UTG_NS_Store.IDUM
left join [dba].ACRegType at2 on at2.ID = SV_ZIA_UTG_NS_StoreOut.IDACReg
union
select 
US_ABA_NS_StoreOutItems.*,
US_ABA_NS_StoreOut.*,
US_ABA_NS_Store.PN,
US_ABA_NS_Store.SN,
US_ABA_NS_Store.ELT_ID,
US_ABA_NS_Store.IDBalanceType,
122 as number_store,
'US_ABA_NS' as name_store,
[DBA].US_ABA_NS_StoreOutItems.id as id_,
[DBA].US_ABA_NS_StoreOutItems.IDSOF as IDSOF_,
[DBA].US_ABA_NS_StoreOut.SOFdate as SOFdate_,
StoreOutTransactions.TransactionType,
[DBA].US_ABA_NS_StoreOut.IDCustomer as IDCustomer_,
[DBA].US_ABA_NS_Store.IDUM as IDum_,
bum.SymbolInt,
at2.RegistrationNumber
from [DBA].US_ABA_NS_StoreOutItems
join [DBA].US_ABA_NS_StoreOut on [DBA].US_ABA_NS_StoreOut.ID = [DBA].US_ABA_NS_StoreOutItems.IDSOF
left join [DBA].SOTransactionsCross on [DBA].SOTransactionsCross.IDStore = number_store and [DBA].SOTransactionsCross.IDSOF = [DBA].US_ABA_NS_StoreOut.ID
left join [DBA].StoreOutTransactions on [DBA].StoreOutTransactions.ID = [DBA].SOTransactionsCross.IDStoreOutTransaction
left join [DBA].US_ABA_NS_Store on [DBA].US_ABA_NS_Store.ELT_BN = [DBA].US_ABA_NS_StoreOutItems.ELT_BN and [DBA].US_ABA_NS_Store.ID = [DBA].US_ABA_NS_StoreOutItems.IDInStoreTable
left join [mma].BasUnMeas bum on bum.ID = US_ABA_NS_Store.IDUM
left join [dba].ACRegType at2 on at2.ID = US_ABA_NS_StoreOut.IDACReg
union
select
US_DME_NS2_StoreOutItems.*,
US_DME_NS2_StoreOut.*,
US_DME_NS2_Store.PN,
US_DME_NS2_Store.SN,
US_DME_NS2_Store.ELT_ID,
US_DME_NS2_Store.IDBalanceType,
107 as number_store,
'US_DME_NS2' as name_store,
[DBA].US_DME_NS2_StoreOutItems.id as id_,
[DBA].US_DME_NS2_StoreOutItems.IDSOF as IDSOF_,
[DBA].US_DME_NS2_StoreOut.SOFdate as SOFdate_,
StoreOutTransactions.TransactionType,
[DBA].US_DME_NS2_StoreOut.IDCustomer as IDCustomer_,
[DBA].US_DME_NS2_Store.IDUM as IDum_,
bum.SymbolInt,
at2.RegistrationNumber
from [DBA].US_DME_NS2_StoreOutItems
join [DBA].US_DME_NS2_StoreOut on [DBA].US_DME_NS2_StoreOut.ID = [DBA].US_DME_NS2_StoreOutItems.IDSOF
left join [DBA].SOTransactionsCross on [DBA].SOTransactionsCross.IDStore = number_store and [DBA].SOTransactionsCross.IDSOF = [DBA].US_DME_NS2_StoreOut.ID
left join [DBA].StoreOutTransactions on [DBA].StoreOutTransactions.ID = [DBA].SOTransactionsCross.IDStoreOutTransaction
left join [DBA].US_DME_NS2_Store on [DBA].US_DME_NS2_Store.ELT_BN = [DBA].US_DME_NS2_StoreOutItems.ELT_BN and [DBA].US_DME_NS2_Store.ID = [DBA].US_DME_NS2_StoreOutItems.IDInStoreTable
left join [mma].BasUnMeas bum on bum.ID = US_DME_NS2_Store.IDUM
left join [dba].ACRegType at2 on at2.ID = US_DME_NS2_StoreOut.IDACReg
union
select 
US_DME_UTG_StoreOutItems.*,
US_DME_UTG_StoreOut.*,
US_DME_UTG_Store.PN,
US_DME_UTG_Store.SN,
US_DME_UTG_Store.ELT_ID,
US_DME_UTG_Store.IDBalanceType,
103 as number_store,
'US_DME_UTG' as name_store,
[DBA].US_DME_UTG_StoreOutItems.id as id_,
[DBA].US_DME_UTG_StoreOutItems.IDSOF as IDSOF_,
[DBA].US_DME_UTG_StoreOut.SOFdate as SOFdate_,
StoreOutTransactions.TransactionType,
[DBA].US_DME_UTG_StoreOut.IDCustomer as IDCustomer_,
[DBA].US_DME_UTG_Store.IDUM as IDum_,
bum.SymbolInt,
at2.RegistrationNumber
from [DBA].US_DME_UTG_StoreOutItems
join [DBA].US_DME_UTG_StoreOut on [DBA].US_DME_UTG_StoreOut.ID = [DBA].US_DME_UTG_StoreOutItems.IDSOF
left join [DBA].SOTransactionsCross on [DBA].SOTransactionsCross.IDStore = number_store and [DBA].SOTransactionsCross.IDSOF = [DBA].US_DME_UTG_StoreOut.ID
left join [DBA].StoreOutTransactions on [DBA].StoreOutTransactions.ID = [DBA].SOTransactionsCross.IDStoreOutTransaction
left join [DBA].US_DME_UTG_Store on [DBA].US_DME_UTG_Store.ELT_BN = [DBA].US_DME_UTG_StoreOutItems.ELT_BN and [DBA].US_DME_UTG_Store.ID = [DBA].US_DME_UTG_StoreOutItems.IDInStoreTable
left join [mma].BasUnMeas bum on bum.ID = US_DME_UTG_Store.IDUM
left join [dba].ACRegType at2 on at2.ID = US_DME_UTG_StoreOut.IDACReg
union
select
US_KJA_NS_StoreOutItems.*,
US_KJA_NS_StoreOut.*,
US_KJA_NS_Store.PN,
US_KJA_NS_Store.SN,
US_KJA_NS_Store.ELT_ID,
US_KJA_NS_Store.IDBalanceType,
105 as number_store,
'US_KJA_NS' as name_store,
[DBA].US_KJA_NS_StoreOutItems.id as id_,
[DBA].US_KJA_NS_StoreOutItems.IDSOF as IDSOF_,
[DBA].US_KJA_NS_StoreOut.SOFdate as SOFdate_,
StoreOutTransactions.TransactionType,
[DBA].US_KJA_NS_StoreOut.IDCustomer as IDCustomer_,
[DBA].US_KJA_NS_Store.IDUM as IDum_,
bum.SymbolInt,
at2.RegistrationNumber
from [DBA].US_KJA_NS_StoreOutItems
join [DBA].US_KJA_NS_StoreOut on [DBA].US_KJA_NS_StoreOut.ID = [DBA].US_KJA_NS_StoreOutItems.IDSOF
left join [DBA].SOTransactionsCross on [DBA].SOTransactionsCross.IDStore = number_store and [DBA].SOTransactionsCross.IDSOF = [DBA].US_KJA_NS_StoreOut.ID
left join [DBA].StoreOutTransactions on [DBA].StoreOutTransactions.ID = [DBA].SOTransactionsCross.IDStoreOutTransaction
left join [DBA].US_KJA_NS_Store on [DBA].US_KJA_NS_Store.ELT_BN = [DBA].US_KJA_NS_StoreOutItems.ELT_BN and [DBA].US_KJA_NS_Store.ID = [DBA].US_KJA_NS_StoreOutItems.IDInStoreTable
left join [mma].BasUnMeas bum on bum.ID = US_KJA_NS_Store.IDUM
left join [dba].ACRegType at2 on at2.ID = US_KJA_NS_StoreOut.IDACReg
union
select 
US_NSK_NS2_StoreOutItems.*,
US_NSK_NS2_StoreOut.*,
US_NSK_NS2_Store.PN,
US_NSK_NS2_Store.SN,
US_NSK_NS2_Store.ELT_ID,
US_NSK_NS2_Store.IDBalanceType,
109 as number_store,
'US_NSK_NS2' as name_store,
[DBA].US_NSK_NS2_StoreOutItems.id as id_,
[DBA].US_NSK_NS2_StoreOutItems.IDSOF as IDSOF_,
[DBA].US_NSK_NS2_StoreOut.SOFdate as SOFdate_,
StoreOutTransactions.TransactionType,
[DBA].US_NSK_NS2_StoreOut.IDCustomer as IDCustomer_,
[DBA].US_NSK_NS2_Store.IDUM as IDum_,
bum.SymbolInt,
at2.RegistrationNumber
from [DBA].US_NSK_NS2_StoreOutItems
join [DBA].US_NSK_NS2_StoreOut on [DBA].US_NSK_NS2_StoreOut.ID = [DBA].US_NSK_NS2_StoreOutItems.IDSOF
left join [DBA].SOTransactionsCross on [DBA].SOTransactionsCross.IDStore = number_store and [DBA].SOTransactionsCross.IDSOF = [DBA].US_NSK_NS2_StoreOut.ID
left join [DBA].StoreOutTransactions on [DBA].StoreOutTransactions.ID = [DBA].SOTransactionsCross.IDStoreOutTransaction
left join [DBA].US_NSK_NS2_Store on [DBA].US_NSK_NS2_Store.ELT_BN = [DBA].US_NSK_NS2_StoreOutItems.ELT_BN and [DBA].US_NSK_NS2_Store.ID = [DBA].US_NSK_NS2_StoreOutItems.IDInStoreTable
left join [mma].BasUnMeas bum on bum.ID = US_NSK_NS2_Store.IDUM
left join [dba].ACRegType at2 on at2.ID = US_NSK_NS2_StoreOut.IDACReg
union
select 
US_NUX_NS_StoreOutItems.*,
US_NUX_NS_StoreOut.*,
US_NUX_NS_Store.PN,
US_NUX_NS_Store.SN,
US_NUX_NS_Store.ELT_ID,
US_NUX_NS_Store.IDBalanceType,
101 as number_store,
'US_NUX_NS' as name_store,
[DBA].US_NUX_NS_StoreOutItems.id as id_,
[DBA].US_NUX_NS_StoreOutItems.IDSOF as IDSOF_,
[DBA].US_NUX_NS_StoreOut.SOFdate as SOFdate_,
StoreOutTransactions.TransactionType,
[DBA].US_NUX_NS_StoreOut.IDCustomer as IDCustomer_,
[DBA].US_NUX_NS_Store.IDUM as IDum_,
bum.SymbolInt,
at2.RegistrationNumber
from [DBA].US_NUX_NS_StoreOutItems
join [DBA].US_NUX_NS_StoreOut on [DBA].US_NUX_NS_StoreOut.ID = [DBA].US_NUX_NS_StoreOutItems.IDSOF
left join [DBA].SOTransactionsCross on [DBA].SOTransactionsCross.IDStore = number_store and [DBA].SOTransactionsCross.IDSOF = [DBA].US_NUX_NS_StoreOut.ID
left join [DBA].StoreOutTransactions on [DBA].StoreOutTransactions.ID = [DBA].SOTransactionsCross.IDStoreOutTransaction
left join [DBA].US_NUX_NS_Store on [DBA].US_NUX_NS_Store.ELT_BN = [DBA].US_NUX_NS_StoreOutItems.ELT_BN and [DBA].US_NUX_NS_Store.ID = [DBA].US_NUX_NS_StoreOutItems.IDInStoreTable
left join [mma].BasUnMeas bum on bum.ID = US_NUX_NS_Store.IDUM
left join [dba].ACRegType at2 on at2.ID = US_NUX_NS_StoreOut.IDACReg
union
select
US_ZIA_NS_StoreOutItems.*,
US_ZIA_NS_StoreOut.*,
US_ZIA_NS_Store.PN,
US_ZIA_NS_Store.SN,
US_ZIA_NS_Store.ELT_ID,
US_ZIA_NS_Store.IDBalanceType,
130 as number_store,
'US_ZIA_NS' as name_store,
[DBA].US_ZIA_NS_StoreOutItems.id as id_,
[DBA].US_ZIA_NS_StoreOutItems.IDSOF as IDSOF_,
[DBA].US_ZIA_NS_StoreOut.SOFdate as SOFdate_,
StoreOutTransactions.TransactionType,
[DBA].US_ZIA_NS_StoreOut.IDCustomer as IDCustomer_,
[DBA].US_ZIA_NS_Store.IDUM as IDum_,
bum.SymbolInt,
at2.RegistrationNumber
from [DBA].US_ZIA_NS_StoreOutItems
join [DBA].US_ZIA_NS_StoreOut on [DBA].US_ZIA_NS_StoreOut.ID = [DBA].US_ZIA_NS_StoreOutItems.IDSOF
left join [DBA].SOTransactionsCross on [DBA].SOTransactionsCross.IDStore = number_store and [DBA].SOTransactionsCross.IDSOF = [DBA].US_ZIA_NS_StoreOut.ID
left join [DBA].StoreOutTransactions on [DBA].StoreOutTransactions.ID = [DBA].SOTransactionsCross.IDStoreOutTransaction
left join [DBA].US_ZIA_NS_Store on [DBA].US_ZIA_NS_Store.ELT_BN = [DBA].US_ZIA_NS_StoreOutItems.ELT_BN and [DBA].US_ZIA_NS_Store.ID = [DBA].US_ZIA_NS_StoreOutItems.IDInStoreTable
left join [mma].BasUnMeas bum on bum.ID = US_ZIA_NS_Store.IDUM
left join [dba].ACRegType at2 on at2.ID = US_ZIA_NS_StoreOut.IDACReg
union
select 
SV_KJA_ATRAN_StoreOutItems.*,
SV_KJA_ATRAN_StoreOut.*,
SV_KJA_ATRAN_Store.PN,
SV_KJA_ATRAN_Store.SN,
SV_KJA_ATRAN_Store.ELT_ID,
SV_KJA_ATRAN_Store.IDBalanceType,
112 as number_store,
'SV_KJA_ATRAN' as name_store,
[DBA].SV_KJA_ATRAN_StoreOutItems.id as id_,
[DBA].SV_KJA_ATRAN_StoreOutItems.IDSOF as IDSOF_,
[DBA].SV_KJA_ATRAN_StoreOut.SOFdate as SOFdate_,
StoreOutTransactions.TransactionType,
[DBA].SV_KJA_ATRAN_StoreOut.IDCustomer as IDCustomer_,
[DBA].SV_KJA_ATRAN_Store.IDUM as IDum_,
bum.SymbolInt,
at2.RegistrationNumber
from [DBA].SV_KJA_ATRAN_StoreOutItems
join [DBA].SV_KJA_ATRAN_StoreOut on [DBA].SV_KJA_ATRAN_StoreOut.ID = [DBA].SV_KJA_ATRAN_StoreOutItems.IDSOF
left join [DBA].SOTransactionsCross on [DBA].SOTransactionsCross.IDStore = number_store and [DBA].SOTransactionsCross.IDSOF = [DBA].SV_KJA_ATRAN_StoreOut.ID
left join [DBA].StoreOutTransactions on [DBA].StoreOutTransactions.ID = [DBA].SOTransactionsCross.IDStoreOutTransaction
left join [DBA].SV_KJA_ATRAN_Store on [DBA].SV_KJA_ATRAN_Store.ELT_BN = [DBA].SV_KJA_ATRAN_StoreOutItems.ELT_BN and [DBA].SV_KJA_ATRAN_Store.ID = [DBA].SV_KJA_ATRAN_StoreOutItems.IDInStoreTable
left join [mma].BasUnMeas bum on bum.ID = SV_KJA_ATRAN_Store.IDUM
left join [dba].ACRegType at2 on at2.ID = SV_KJA_ATRAN_StoreOut.IDACReg
union
select 
US_KJA_ATRAN_StoreOutItems.*,
US_KJA_ATRAN_StoreOut.*,
US_KJA_ATRAN_Store.PN,
US_KJA_ATRAN_Store.SN,
US_KJA_ATRAN_Store.ELT_ID,
US_KJA_ATRAN_Store.IDBalanceType,
113 as number_store,
'US_KJA_ATRAN' as name_store,
[DBA].US_KJA_ATRAN_StoreOutItems.id as id_,
[DBA].US_KJA_ATRAN_StoreOutItems.IDSOF as IDSOF_,
[DBA].US_KJA_ATRAN_StoreOut.SOFdate as SOFdate_,
StoreOutTransactions.TransactionType,
[DBA].US_KJA_ATRAN_StoreOut.IDCustomer as IDCustomer_,
[DBA].US_KJA_ATRAN_Store.IDUM as IDum_,
bum.SymbolInt,
at2.RegistrationNumber
from [DBA].US_KJA_ATRAN_StoreOutItems
join [DBA].US_KJA_ATRAN_StoreOut on [DBA].US_KJA_ATRAN_StoreOut.ID = [DBA].US_KJA_ATRAN_StoreOutItems.IDSOF
left join [DBA].SOTransactionsCross on [DBA].SOTransactionsCross.IDStore = number_store and [DBA].SOTransactionsCross.IDSOF = [DBA].US_KJA_ATRAN_StoreOut.ID
left join [DBA].StoreOutTransactions on [DBA].StoreOutTransactions.ID = [DBA].SOTransactionsCross.IDStoreOutTransaction
left join [DBA].US_KJA_ATRAN_Store on [DBA].US_KJA_ATRAN_Store.ELT_BN = [DBA].US_KJA_ATRAN_StoreOutItems.ELT_BN and [DBA].US_KJA_ATRAN_Store.ID = [DBA].US_KJA_ATRAN_StoreOutItems.IDInStoreTable
left join [mma].BasUnMeas bum on bum.ID = US_KJA_ATRAN_Store.IDUM
left join [dba].ACRegType at2 on at2.ID = US_KJA_ATRAN_StoreOut.IDACReg
union
select
US_KJA_KA_StoreOutItems.*,
US_KJA_KA_StoreOut.*,
US_KJA_KA_Store.PN,
US_KJA_KA_Store.SN,
US_KJA_KA_Store.ELT_ID,
US_KJA_KA_Store.IDBalanceType,
125 as number_store,
'US_KJA_KA' as name_store,
[DBA].US_KJA_KA_StoreOutItems.id as id_,
[DBA].US_KJA_KA_StoreOutItems.IDSOF as IDSOF_,
[DBA].US_KJA_KA_StoreOut.SOFdate as SOFdate_,
StoreOutTransactions.TransactionType,
[DBA].US_KJA_KA_StoreOut.IDCustomer as IDCustomer_,
[DBA].US_KJA_KA_Store.IDUM as IDum_,
bum.SymbolInt,
at2.RegistrationNumber
from [DBA].US_KJA_KA_StoreOutItems
join [DBA].US_KJA_KA_StoreOut on [DBA].US_KJA_KA_StoreOut.ID = [DBA].US_KJA_KA_StoreOutItems.IDSOF
left join [DBA].SOTransactionsCross on [DBA].SOTransactionsCross.IDStore = number_store and [DBA].SOTransactionsCross.IDSOF = [DBA].US_KJA_KA_StoreOut.ID
left join [DBA].StoreOutTransactions on [DBA].StoreOutTransactions.ID = [DBA].SOTransactionsCross.IDStoreOutTransaction
left join [DBA].US_KJA_KA_Store on [DBA].US_KJA_KA_Store.ELT_BN = [DBA].US_KJA_KA_StoreOutItems.ELT_BN and [DBA].US_KJA_KA_Store.ID = [DBA].US_KJA_KA_StoreOutItems.IDInStoreTable
left join [mma].BasUnMeas bum on bum.ID = US_KJA_KA_Store.IDUM
left join [dba].ACRegType at2 on at2.ID = US_KJA_KA_StoreOut.IDACReg
union
select 
SV_NSK_UT_StoreOutItems.*,
SV_NSK_UT_StoreOut.*,
SV_NSK_UT_Store.PN,
SV_NSK_UT_Store.SN,
SV_NSK_UT_Store.ELT_ID,
SV_NSK_UT_Store.IDBalanceType,
127 as number_store,
'SV_NSK_UT' as name_store,
[DBA].SV_NSK_UT_StoreOutItems.id as id_,
[DBA].SV_NSK_UT_StoreOutItems.IDSOF as IDSOF_,
[DBA].SV_NSK_UT_StoreOut.SOFdate as SOFdate_,
StoreOutTransactions.TransactionType,
[DBA].SV_NSK_UT_StoreOut.IDCustomer as IDCustomer_,
[DBA].SV_NSK_UT_Store.IDUM as IDum_,
bum.SymbolInt,
at2.RegistrationNumber
from [DBA].SV_NSK_UT_StoreOutItems
join [DBA].SV_NSK_UT_StoreOut on [DBA].SV_NSK_UT_StoreOut.ID = [DBA].SV_NSK_UT_StoreOutItems.IDSOF
left join [DBA].SOTransactionsCross on [DBA].SOTransactionsCross.IDStore = number_store and [DBA].SOTransactionsCross.IDSOF = [DBA].SV_NSK_UT_StoreOut.ID
left join [DBA].StoreOutTransactions on [DBA].StoreOutTransactions.ID = [DBA].SOTransactionsCross.IDStoreOutTransaction
left join [DBA].SV_NSK_UT_Store on [DBA].SV_NSK_UT_Store.ELT_BN = [DBA].SV_NSK_UT_StoreOutItems.ELT_BN and [DBA].SV_NSK_UT_Store.ID = [DBA].SV_NSK_UT_StoreOutItems.IDInStoreTable
left join [mma].BasUnMeas bum on bum.ID = SV_NSK_UT_Store.IDUM
left join [dba].ACRegType at2 on at2.ID = SV_NSK_UT_StoreOut.IDACReg
union
select
US_NSK_UT_StoreOutItems.*,
US_NSK_UT_StoreOut.*,
US_NSK_UT_Store.PN,
US_NSK_UT_Store.SN,
US_NSK_UT_Store.ELT_ID,
US_NSK_UT_Store.IDBalanceType,
128 as number_store,
'US_NSK_UT' as name_store,
[DBA].US_NSK_UT_StoreOutItems.id as id_,
[DBA].US_NSK_UT_StoreOutItems.IDSOF as IDSOF_,
[DBA].US_NSK_UT_StoreOut.SOFdate as SOFdate_,
StoreOutTransactions.TransactionType,
[DBA].US_NSK_UT_StoreOut.IDCustomer as IDCustomer_,
[DBA].US_NSK_UT_Store.IDUM as IDum_,
bum.SymbolInt,
at2.RegistrationNumber
from [DBA].US_NSK_UT_StoreOutItems
join [DBA].US_NSK_UT_StoreOut on [DBA].US_NSK_UT_StoreOut.ID = [DBA].US_NSK_UT_StoreOutItems.IDSOF
left join [DBA].SOTransactionsCross on [DBA].SOTransactionsCross.IDStore = number_store and [DBA].SOTransactionsCross.IDSOF = [DBA].US_NSK_UT_StoreOut.ID
left join [DBA].StoreOutTransactions on [DBA].StoreOutTransactions.ID = [DBA].SOTransactionsCross.IDStoreOutTransaction
left join [DBA].US_NSK_UT_Store on [DBA].US_NSK_UT_Store.ELT_BN = [DBA].US_NSK_UT_StoreOutItems.ELT_BN and [DBA].US_NSK_UT_Store.ID = [DBA].US_NSK_UT_StoreOutItems.IDInStoreTable
left join [mma].BasUnMeas bum on bum.ID = US_NSK_UT_Store.IDUM
left join [dba].ACRegType at2 on at2.ID = US_NSK_UT_StoreOut.IDACReg
union
select
US_ZIA_UTG_NS_StoreOutItems.*,
US_ZIA_UTG_NS_StoreOut.*,
US_ZIA_UTG_NS_Store.PN,
US_ZIA_UTG_NS_Store.SN,
US_ZIA_UTG_NS_Store.ELT_ID,
US_ZIA_UTG_NS_Store.IDBalanceType,
133 as number_store,
'US_ZIA_UTG_NS' as name_store,
[DBA].US_ZIA_UTG_NS_StoreOutItems.id as id_,
[DBA].US_ZIA_UTG_NS_StoreOutItems.IDSOF as IDSOF_,
[DBA].US_ZIA_UTG_NS_StoreOut.SOFdate as SOFdate_,
StoreOutTransactions.TransactionType,
[DBA].US_ZIA_UTG_NS_StoreOut.IDCustomer as IDCustomer_,
[DBA].US_ZIA_UTG_NS_Store.IDUM as IDum_,
bum.SymbolInt,
at2.RegistrationNumber
from [DBA].US_ZIA_UTG_NS_StoreOutItems
join [DBA].US_ZIA_UTG_NS_StoreOut on [DBA].US_ZIA_UTG_NS_StoreOut.ID = [DBA].US_ZIA_UTG_NS_StoreOutItems.IDSOF
left join [DBA].SOTransactionsCross on [DBA].SOTransactionsCross.IDStore = number_store and [DBA].SOTransactionsCross.IDSOF = [DBA].US_ZIA_UTG_NS_StoreOut.ID
left join [DBA].StoreOutTransactions on [DBA].StoreOutTransactions.ID = [DBA].SOTransactionsCross.IDStoreOutTransaction
left join [DBA].US_ZIA_UTG_NS_Store on [DBA].US_ZIA_UTG_NS_Store.ELT_BN = [DBA].US_ZIA_UTG_NS_StoreOutItems.ELT_BN and [DBA].US_ZIA_UTG_NS_Store.ID = [DBA].US_ZIA_UTG_NS_StoreOutItems.IDInStoreTable
left join [mma].BasUnMeas bum on bum.ID = US_ZIA_UTG_NS_Store.IDUM
left join [dba].ACRegType at2 on at2.ID = US_ZIA_UTG_NS_StoreOut.IDACReg
union
select
SV_DME_KRLOG_StoreOutItems.*,
SV_DME_KRLOG_StoreOut.*,
SV_DME_KRLOG_Store.PN,
SV_DME_KRLOG_Store.SN,
SV_DME_KRLOG_Store.ELT_ID,
SV_DME_KRLOG_Store.IDBalanceType,
134 as number_store,
'SV_DME_KRLOG' as name_store,
[DBA].SV_DME_KRLOG_StoreOutItems.id as id_,
[DBA].SV_DME_KRLOG_StoreOutItems.IDSOF as IDSOF_,
[DBA].SV_DME_KRLOG_StoreOut.SOFdate as SOFdate_,
StoreOutTransactions.TransactionType,
[DBA].SV_DME_KRLOG_StoreOut.IDCustomer as IDCustomer_,
[DBA].SV_DME_KRLOG_Store.IDUM as IDum_,
bum.SymbolInt,
at2.RegistrationNumber
from [DBA].SV_DME_KRLOG_StoreOutItems
join [DBA].SV_DME_KRLOG_StoreOut on [DBA].SV_DME_KRLOG_StoreOut.ID = [DBA].SV_DME_KRLOG_StoreOutItems.IDSOF
left join [DBA].SOTransactionsCross on [DBA].SOTransactionsCross.IDStore = number_store and [DBA].SOTransactionsCross.IDSOF = [DBA].SV_DME_KRLOG_StoreOut.ID
left join [DBA].StoreOutTransactions on [DBA].StoreOutTransactions.ID = [DBA].SOTransactionsCross.IDStoreOutTransaction
left join [DBA].SV_DME_KRLOG_Store on [DBA].SV_DME_KRLOG_Store.ELT_BN = [DBA].SV_DME_KRLOG_StoreOutItems.ELT_BN and [DBA].SV_DME_KRLOG_Store.ID = [DBA].SV_DME_KRLOG_StoreOutItems.IDInStoreTable
left join [mma].BasUnMeas bum on bum.ID = SV_DME_KRLOG_Store.IDUM
left join [dba].ACRegType at2 on at2.ID = SV_DME_KRLOG_StoreOut.IDACReg
union
select
US_DME_KRLOG_StoreOutItems.*,
US_DME_KRLOG_StoreOut.*,
US_DME_KRLOG_Store.PN,
US_DME_KRLOG_Store.SN,
US_DME_KRLOG_Store.ELT_ID,
US_DME_KRLOG_Store.IDBalanceType,
135 as number_store,
'US_DME_KRLOG' as name_store,
[DBA].US_DME_KRLOG_StoreOutItems.id as id_,
[DBA].US_DME_KRLOG_StoreOutItems.IDSOF as IDSOF_,
[DBA].US_DME_KRLOG_StoreOut.SOFdate as SOFdate_,
StoreOutTransactions.TransactionType,
[DBA].US_DME_KRLOG_StoreOut.IDCustomer as IDCustomer_,
[DBA].US_DME_KRLOG_Store.IDUM as IDum_,
bum.SymbolInt,
at2.RegistrationNumber
from [DBA].US_DME_KRLOG_StoreOutItems
join [DBA].US_DME_KRLOG_StoreOut on [DBA].US_DME_KRLOG_StoreOut.ID = [DBA].US_DME_KRLOG_StoreOutItems.IDSOF
left join [DBA].SOTransactionsCross on [DBA].SOTransactionsCross.IDStore = number_store and [DBA].SOTransactionsCross.IDSOF = [DBA].US_DME_KRLOG_StoreOut.ID
left join [DBA].StoreOutTransactions on [DBA].StoreOutTransactions.ID = [DBA].SOTransactionsCross.IDStoreOutTransaction
left join [DBA].US_DME_KRLOG_Store on [DBA].US_DME_KRLOG_Store.ELT_BN = [DBA].US_DME_KRLOG_StoreOutItems.ELT_BN and [DBA].US_DME_KRLOG_Store.ID = [DBA].US_DME_KRLOG_StoreOutItems.IDInStoreTable
left join [mma].BasUnMeas bum on bum.ID = US_DME_KRLOG_Store.IDUM
left join [dba].ACRegType at2 on at2.ID = US_DME_KRLOG_StoreOut.IDACReg
)t
union
select 
number_store,
name_store,
IDMJSS,
t2.id_,
ELT_BN,
ELT_ID,
QTY_Released,
QTY_Restocked,
t2.IDSOF_,
t2.SOFdate_,
registrationnumber,
IDPROPERTY,
Symbolint,
pn,
sn,
TransactionType,
IDBalanceType,
IDCustomer_,
IDum_
from(
select
4 as number_store,
'US_KJA' as name_store,
[DBA].US_KJA_StoreOut.IDMJSS,
[DBA].US_KJA_StoreOutItems.id as id_,
[DBA].US_KJA_StoreOutItems.ELT_BN,
[DBA].US_KJA_Store.ELT_ID,
[DBA].US_KJA_StoreOutItems.QTY_Released,
[DBA].US_KJA_StoreOutItems.QTY_Restocked,
[DBA].US_KJA_StoreOutItems.IDSOF as IDSOF_,
[DBA].US_KJA_StoreOut.SOFdate as SOFdate_,
at2.RegistrationNumber,
[DBA].US_KJA_StoreOutItems.IDProperty,
bum.SymbolInt,
[dba].US_KJA_Store.PN,
[dba].US_KJA_Store.SN,
StoreOutTransactions.TransactionType,
[DBA].US_KJA_StoreOut.IDCustomer as IDCustomer_,
[dba].US_KJA_Store.IDBalanceType,
[DBA].US_KJA_Store.IDUM as IDum_
from [DBA].US_KJA_StoreOutItems
join [DBA].US_KJA_StoreOut on [DBA].US_KJA_StoreOut.ID = [DBA].US_KJA_StoreOutItems.IDSOF
left join [DBA].SOTransactionsCross on [DBA].SOTransactionsCross.IDStore = number_store and [DBA].SOTransactionsCross.IDSOF = [DBA].US_KJA_StoreOut.ID
left join [DBA].StoreOutTransactions on [DBA].StoreOutTransactions.ID = [DBA].SOTransactionsCross.IDStoreOutTransaction
left join [DBA].US_KJA_Store on [DBA].US_KJA_Store.ELT_BN = [DBA].US_KJA_StoreOutItems.ELT_BN and [DBA].US_KJA_Store.ID = [DBA].US_KJA_StoreOutItems.IDInStoreTable
left join [mma].BasUnMeas bum on bum.ID = US_KJA_Store.IDUM
left join [dba].ACRegType at2 on at2.ID = US_KJA_StoreOut.IDACReg
union
select
32 as number_store,
'SV_KJA_UT' as name_store,
[DBA].SV_KJA_UT_StoreOut.IDMJSS,
[DBA].SV_KJA_UT_StoreOutItems.id as id_,
[DBA].SV_KJA_UT_StoreOutItems.ELT_BN,
[DBA].SV_KJA_UT_Store.ELT_ID,
[DBA].SV_KJA_UT_StoreOutItems.QTY_Released,
[DBA].SV_KJA_UT_StoreOutItems.QTY_Restocked,
[DBA].SV_KJA_UT_StoreOutItems.IDSOF as IDSOF_,
[DBA].SV_KJA_UT_StoreOut.SOFdate as SOFdate_,
at2.RegistrationNumber,
[DBA].SV_KJA_UT_StoreOutItems.IDProperty,
bum.SymbolInt,
[dba].SV_KJA_UT_Store.PN,
[dba].SV_KJA_UT_Store.SN,
StoreOutTransactions.TransactionType,
[DBA].SV_KJA_UT_StoreOut.IDCustomer as IDCustomer_,
[dba].SV_KJA_UT_Store.IDBalanceType,
[DBA].SV_KJA_UT_Store.IDUM as IDum_
from [DBA].SV_KJA_UT_StoreOutItems
join [DBA].SV_KJA_UT_StoreOut on [DBA].SV_KJA_UT_StoreOut.ID = [DBA].SV_KJA_UT_StoreOutItems.IDSOF
left join [DBA].SOTransactionsCross on [DBA].SOTransactionsCross.IDStore = number_store and [DBA].SOTransactionsCross.IDSOF = [DBA].SV_KJA_UT_StoreOut.ID
left join [DBA].StoreOutTransactions on [DBA].StoreOutTransactions.ID = [DBA].SOTransactionsCross.IDStoreOutTransaction
left join [DBA].SV_KJA_UT_Store on [DBA].SV_KJA_UT_Store.ELT_BN = [DBA].SV_KJA_UT_StoreOutItems.ELT_BN and [DBA].SV_KJA_UT_Store.ID = [DBA].SV_KJA_UT_StoreOutItems.IDInStoreTable
left join [mma].BasUnMeas bum on bum.ID = SV_KJA_UT_Store.IDUM
left join [dba].ACRegType at2 on at2.ID = SV_KJA_UT_StoreOut.IDACReg
union
select
33 as number_store,
'US_KJA_UT' as name_store,
[DBA].US_KJA_UT_StoreOut.IDMJSS,
[DBA].US_KJA_UT_StoreOutItems.id as id_,
[DBA].US_KJA_UT_StoreOutItems.ELT_BN,
[DBA].US_KJA_UT_Store.ELT_ID,
[DBA].US_KJA_UT_StoreOutItems.QTY_Released,
[DBA].US_KJA_UT_StoreOutItems.QTY_Restocked,
[DBA].US_KJA_UT_StoreOutItems.IDSOF as IDSOF_,
[DBA].US_KJA_UT_StoreOut.SOFdate as SOFdate_,
at2.RegistrationNumber,
[DBA].US_KJA_UT_StoreOutItems.IDProperty,
bum.SymbolInt,
[dba].US_KJA_UT_Store.PN,
[dba].US_KJA_UT_Store.SN,
StoreOutTransactions.TransactionType,
[DBA].US_KJA_UT_StoreOut.IDCustomer as IDCustomer_,
[dba].US_KJA_UT_Store.IDBalanceType,
[DBA].US_KJA_UT_Store.IDUM as IDum_
from [DBA].US_KJA_UT_StoreOutItems
join [DBA].US_KJA_UT_StoreOut on [DBA].US_KJA_UT_StoreOut.ID = [DBA].US_KJA_UT_StoreOutItems.IDSOF
left join [DBA].SOTransactionsCross on [DBA].SOTransactionsCross.IDStore = number_store and [DBA].SOTransactionsCross.IDSOF = [DBA].US_KJA_UT_StoreOut.ID
left join [DBA].StoreOutTransactions on [DBA].StoreOutTransactions.ID = [DBA].SOTransactionsCross.IDStoreOutTransaction
left join [DBA].US_KJA_UT_Store on [DBA].US_KJA_UT_Store.ELT_BN = [DBA].US_KJA_UT_StoreOutItems.ELT_BN and [DBA].US_KJA_UT_Store.ID = [DBA].US_KJA_UT_StoreOutItems.IDInStoreTable
left join [mma].BasUnMeas bum on bum.ID = US_KJA_UT_Store.IDUM
left join [dba].ACRegType at2 on at2.ID = US_KJA_UT_StoreOut.IDACReg
union
select
35 as number_store,
'SV_DME_NS' as name_store,
[DBA].SV_DME_NS_StoreOut.IDMJSS,
[DBA].SV_DME_NS_StoreOutItems.id as id_,
[DBA].SV_DME_NS_StoreOutItems.ELT_BN,
[DBA].SV_DME_NS_Store.ELT_ID,
[DBA].SV_DME_NS_StoreOutItems.QTY_Released,
[DBA].SV_DME_NS_StoreOutItems.QTY_Restocked,
[DBA].SV_DME_NS_StoreOutItems.IDSOF as IDSOF_,
[DBA].SV_DME_NS_StoreOut.SOFdate as SOFdate_,
at2.RegistrationNumber,
[DBA].SV_DME_NS_StoreOutItems.IDProperty,
bum.SymbolInt,
[dba].SV_DME_NS_Store.PN,
[dba].SV_DME_NS_Store.SN,
StoreOutTransactions.TransactionType,
[DBA].SV_DME_NS_StoreOut.IDCustomer as IDCustomer_,
[dba].SV_DME_NS_Store.IDBalanceType,
[DBA].SV_DME_NS_Store.IDUM as IDum_
from [DBA].SV_DME_NS_StoreOutItems
join [DBA].SV_DME_NS_StoreOut on [DBA].SV_DME_NS_StoreOut.ID = [DBA].SV_DME_NS_StoreOutItems.IDSOF
left join [DBA].SOTransactionsCross on [DBA].SOTransactionsCross.IDStore = number_store and [DBA].SOTransactionsCross.IDSOF = [DBA].SV_DME_NS_StoreOut.ID
left join [DBA].StoreOutTransactions on [DBA].StoreOutTransactions.ID = [DBA].SOTransactionsCross.IDStoreOutTransaction
left join [DBA].SV_DME_NS_Store on [DBA].SV_DME_NS_Store.ELT_BN = [DBA].SV_DME_NS_StoreOutItems.ELT_BN and [DBA].SV_DME_NS_Store.ID = [DBA].SV_DME_NS_StoreOutItems.IDInStoreTable
left join [mma].BasUnMeas bum on bum.ID = SV_DME_NS_Store.IDUM
left join [dba].ACRegType at2 on at2.ID = SV_DME_NS_StoreOut.IDACReg
union
select
67 as number_store,
'SV_NSK_NS' as name_store,
[DBA].SV_NSK_NS_StoreOut.IDMJSS,
[DBA].SV_NSK_NS_StoreOutItems.id as id_,
[DBA].SV_NSK_NS_StoreOutItems.ELT_BN,
[DBA].SV_NSK_NS_Store.ELT_ID,
[DBA].SV_NSK_NS_StoreOutItems.QTY_Released,
[DBA].SV_NSK_NS_StoreOutItems.QTY_Restocked,
[DBA].SV_NSK_NS_StoreOutItems.IDSOF as IDSOF_,
[DBA].SV_NSK_NS_StoreOut.SOFdate as SOFdate_,
at2.RegistrationNumber,
[DBA].SV_NSK_NS_StoreOutItems.IDProperty,
bum.SymbolInt,
[dba].SV_NSK_NS_Store.PN,
[dba].SV_NSK_NS_Store.SN,
StoreOutTransactions.TransactionType,
[DBA].SV_NSK_NS_StoreOut.IDCustomer as IDCustomer_,
[dba].SV_NSK_NS_Store.IDBalanceType,
[DBA].SV_NSK_NS_Store.IDUM as IDum_
from [DBA].SV_NSK_NS_StoreOutItems
join [DBA].SV_NSK_NS_StoreOut on [DBA].SV_NSK_NS_StoreOut.ID = [DBA].SV_NSK_NS_StoreOutItems.IDSOF
left join [DBA].SOTransactionsCross on [DBA].SOTransactionsCross.IDStore = number_store and [DBA].SOTransactionsCross.IDSOF = [DBA].SV_NSK_NS_StoreOut.ID
left join [DBA].StoreOutTransactions on [DBA].StoreOutTransactions.ID = [DBA].SOTransactionsCross.IDStoreOutTransaction
left join [DBA].SV_NSK_NS_Store on [DBA].SV_NSK_NS_Store.ELT_BN = [DBA].SV_NSK_NS_StoreOutItems.ELT_BN and [DBA].SV_NSK_NS_Store.ID = [DBA].SV_NSK_NS_StoreOutItems.IDInStoreTable
left join [mma].BasUnMeas bum on bum.ID = SV_NSK_NS_Store.IDUM
left join [dba].ACRegType at2 on at2.ID = SV_NSK_NS_StoreOut.IDACReg
union
select
69 as number_store,
'SV_OVB_NS' as name_store,
[DBA].SV_OVB_NS_StoreOut.IDMJSS,
[DBA].SV_OVB_NS_StoreOutItems.id as id_,
[DBA].SV_OVB_NS_StoreOutItems.ELT_BN,
[DBA].SV_OVB_NS_Store.ELT_ID,
[DBA].SV_OVB_NS_StoreOutItems.QTY_Released,
[DBA].SV_OVB_NS_StoreOutItems.QTY_Restocked,
[DBA].SV_OVB_NS_StoreOutItems.IDSOF as IDSOF_,
[DBA].SV_OVB_NS_StoreOut.SOFdate as SOFdate_,
at2.RegistrationNumber,
[DBA].SV_OVB_NS_StoreOutItems.IDProperty,
bum.SymbolInt,
[dba].SV_OVB_NS_Store.PN,
[dba].SV_OVB_NS_Store.SN,
StoreOutTransactions.TransactionType,
[DBA].SV_OVB_NS_StoreOut.IDCustomer as IDCustomer_,
[dba].SV_OVB_NS_Store.IDBalanceType,
[DBA].SV_OVB_NS_Store.IDUM as IDum_
from [DBA].SV_OVB_NS_StoreOutItems
join [DBA].SV_OVB_NS_StoreOut on [DBA].SV_OVB_NS_StoreOut.ID = [DBA].SV_OVB_NS_StoreOutItems.IDSOF
left join [DBA].SOTransactionsCross on [DBA].SOTransactionsCross.IDStore = number_store and [DBA].SOTransactionsCross.IDSOF = [DBA].SV_OVB_NS_StoreOut.ID
left join [DBA].StoreOutTransactions on [DBA].StoreOutTransactions.ID = [DBA].SOTransactionsCross.IDStoreOutTransaction
left join [DBA].SV_OVB_NS_Store on [DBA].SV_OVB_NS_Store.ELT_BN = [DBA].SV_OVB_NS_StoreOutItems.ELT_BN and [DBA].SV_OVB_NS_Store.ID = [DBA].SV_OVB_NS_StoreOutItems.IDInStoreTable
left join [mma].BasUnMeas bum on bum.ID = SV_OVB_NS_Store.IDUM
left join [dba].ACRegType at2 on at2.ID = SV_OVB_NS_StoreOut.IDACReg
union
select
13 as number_store,
'SV_SVO_NS' as name_store,
[DBA].SV_SVO_NS_StoreOut.IDMJSS,
[DBA].SV_SVO_NS_StoreOutItems.id as id_,
[DBA].SV_SVO_NS_StoreOutItems.ELT_BN,
[DBA].SV_SVO_NS_Store.ELT_ID,
[DBA].SV_SVO_NS_StoreOutItems.QTY_Released,
[DBA].SV_SVO_NS_StoreOutItems.QTY_Restocked,
[DBA].SV_SVO_NS_StoreOutItems.IDSOF as IDSOF_,
[DBA].SV_SVO_NS_StoreOut.SOFdate as SOFdate_,
at2.RegistrationNumber,
[DBA].SV_SVO_NS_StoreOutItems.IDProperty,
bum.SymbolInt,
[dba].SV_SVO_NS_Store.PN,
[dba].SV_SVO_NS_Store.SN,
StoreOutTransactions.TransactionType,
[DBA].SV_SVO_NS_StoreOut.IDCustomer as IDCustomer_,
[dba].SV_SVO_NS_Store.IDBalanceType,
[DBA].SV_SVO_NS_Store.IDUM as IDum_
from [DBA].SV_SVO_NS_StoreOutItems
join [DBA].SV_SVO_NS_StoreOut on [DBA].SV_SVO_NS_StoreOut.ID = [DBA].SV_SVO_NS_StoreOutItems.IDSOF
left join [DBA].SOTransactionsCross on [DBA].SOTransactionsCross.IDStore = number_store and [DBA].SOTransactionsCross.IDSOF = [DBA].SV_SVO_NS_StoreOut.ID
left join [DBA].StoreOutTransactions on [DBA].StoreOutTransactions.ID = [DBA].SOTransactionsCross.IDStoreOutTransaction
left join [DBA].SV_SVO_NS_Store on [DBA].SV_SVO_NS_Store.ELT_BN = [DBA].SV_SVO_NS_StoreOutItems.ELT_BN and [DBA].SV_SVO_NS_Store.ID = [DBA].SV_SVO_NS_StoreOutItems.IDInStoreTable
left join [mma].BasUnMeas bum on bum.ID = SV_SVO_NS_Store.IDUM
left join [dba].ACRegType at2 on at2.ID = SV_SVO_NS_StoreOut.IDACReg
union
select
36 as number_store,
'US_DME_NS' as name_store,
[DBA].US_DME_NS_StoreOut.IDMJSS,
[DBA].US_DME_NS_StoreOutItems.id as id_,
[DBA].US_DME_NS_StoreOutItems.ELT_BN,
[DBA].US_DME_NS_Store.ELT_ID,
[DBA].US_DME_NS_StoreOutItems.QTY_Released,
[DBA].US_DME_NS_StoreOutItems.QTY_Restocked,
[DBA].US_DME_NS_StoreOutItems.IDSOF as IDSOF_,
[DBA].US_DME_NS_StoreOut.SOFdate as SOFdate_,
at2.RegistrationNumber,
[DBA].US_DME_NS_StoreOutItems.IDProperty,
bum.SymbolInt,
[dba].US_DME_NS_Store.PN,
[dba].US_DME_NS_Store.SN,
StoreOutTransactions.TransactionType,
[DBA].US_DME_NS_StoreOut.IDCustomer as IDCustomer_,
[dba].US_DME_NS_Store.IDBalanceType,
[DBA].US_DME_NS_Store.IDUM as IDum_
from [DBA].US_DME_NS_StoreOutItems
join [DBA].US_DME_NS_StoreOut on [DBA].US_DME_NS_StoreOut.ID = [DBA].US_DME_NS_StoreOutItems.IDSOF
left join [DBA].SOTransactionsCross on [DBA].SOTransactionsCross.IDStore = number_store and [DBA].SOTransactionsCross.IDSOF = [DBA].US_DME_NS_StoreOut.ID
left join [DBA].StoreOutTransactions on [DBA].StoreOutTransactions.ID = [DBA].SOTransactionsCross.IDStoreOutTransaction
left join [DBA].US_DME_NS_Store on [DBA].US_DME_NS_Store.ELT_BN = [DBA].US_DME_NS_StoreOutItems.ELT_BN and [DBA].US_DME_NS_Store.ID = [DBA].US_DME_NS_StoreOutItems.IDInStoreTable
left join [mma].BasUnMeas bum on bum.ID = US_DME_NS_Store.IDUM
left join [dba].ACRegType at2 on at2.ID = US_DME_NS_StoreOut.IDACReg
union
select
68 as number_store,
'US_NSK_NS' as name_store,
[DBA].US_NSK_NS_StoreOut.IDMJSS,
[DBA].US_NSK_NS_StoreOutItems.id as id_,
[DBA].US_NSK_NS_StoreOutItems.ELT_BN,
[DBA].US_NSK_NS_Store.ELT_ID,
[DBA].US_NSK_NS_StoreOutItems.QTY_Released,
[DBA].US_NSK_NS_StoreOutItems.QTY_Restocked,
[DBA].US_NSK_NS_StoreOutItems.IDSOF as IDSOF_,
[DBA].US_NSK_NS_StoreOut.SOFdate as SOFdate_,
at2.RegistrationNumber,
[DBA].US_NSK_NS_StoreOutItems.IDProperty,
bum.SymbolInt,
[dba].US_NSK_NS_Store.PN,
[dba].US_NSK_NS_Store.SN,
StoreOutTransactions.TransactionType,
[DBA].US_NSK_NS_StoreOut.IDCustomer as IDCustomer_,
[dba].US_NSK_NS_Store.IDBalanceType,
[DBA].US_NSK_NS_Store.IDUM as IDum_
from [DBA].US_NSK_NS_StoreOutItems
join [DBA].US_NSK_NS_StoreOut on [DBA].US_NSK_NS_StoreOut.ID = [DBA].US_NSK_NS_StoreOutItems.IDSOF
left join [DBA].SOTransactionsCross on [DBA].SOTransactionsCross.IDStore = number_store and [DBA].SOTransactionsCross.IDSOF = [DBA].US_NSK_NS_StoreOut.ID
left join [DBA].StoreOutTransactions on [DBA].StoreOutTransactions.ID = [DBA].SOTransactionsCross.IDStoreOutTransaction
left join [DBA].US_NSK_NS_Store on [DBA].US_NSK_NS_Store.ELT_BN = [DBA].US_NSK_NS_StoreOutItems.ELT_BN and [DBA].US_NSK_NS_Store.ID = [DBA].US_NSK_NS_StoreOutItems.IDInStoreTable
left join [mma].BasUnMeas bum on bum.ID = US_NSK_NS_Store.IDUM
left join [dba].ACRegType at2 on at2.ID = US_NSK_NS_StoreOut.IDACReg
union
select
70 as number_store,
'US_OVB_NS' as name_store,
[DBA].US_OVB_NS_StoreOut.IDMJSS,
[DBA].US_OVB_NS_StoreOutItems.id as id_,
[DBA].US_OVB_NS_StoreOutItems.ELT_BN,
[DBA].US_OVB_NS_Store.ELT_ID,
[DBA].US_OVB_NS_StoreOutItems.QTY_Released,
[DBA].US_OVB_NS_StoreOutItems.QTY_Restocked,
[DBA].US_OVB_NS_StoreOutItems.IDSOF as IDSOF_,
[DBA].US_OVB_NS_StoreOut.SOFdate as SOFdate_,
at2.RegistrationNumber,
[DBA].US_OVB_NS_StoreOutItems.IDProperty,
bum.SymbolInt,
[dba].US_OVB_NS_Store.PN,
[dba].US_OVB_NS_Store.SN,
StoreOutTransactions.TransactionType,
[DBA].US_OVB_NS_StoreOut.IDCustomer as IDCustomer_,
[dba].US_OVB_NS_Store.IDBalanceType,
[DBA].US_OVB_NS_Store.IDUM as IDum_
from [DBA].US_OVB_NS_StoreOutItems
join [DBA].US_OVB_NS_StoreOut on [DBA].US_OVB_NS_StoreOut.ID = [DBA].US_OVB_NS_StoreOutItems.IDSOF
left join [DBA].SOTransactionsCross on [DBA].SOTransactionsCross.IDStore = number_store and [DBA].SOTransactionsCross.IDSOF = [DBA].US_OVB_NS_StoreOut.ID
left join [DBA].StoreOutTransactions on [DBA].StoreOutTransactions.ID = [DBA].SOTransactionsCross.IDStoreOutTransaction
left join [DBA].US_OVB_NS_Store on [DBA].US_OVB_NS_Store.ELT_BN = [DBA].US_OVB_NS_StoreOutItems.ELT_BN and [DBA].US_OVB_NS_Store.ID = [DBA].US_OVB_NS_StoreOutItems.IDInStoreTable
left join [mma].BasUnMeas bum on bum.ID = US_OVB_NS_Store.IDUM
left join [dba].ACRegType at2 on at2.ID = US_OVB_NS_StoreOut.IDACReg
union
select
14 as number_store,
'US_SVO_NS' as name_store,
[DBA].US_SVO_NS_StoreOut.IDMJSS,
[DBA].US_SVO_NS_StoreOutItems.id as id_,
[DBA].US_SVO_NS_StoreOutItems.ELT_BN,
[DBA].US_SVO_NS_Store.ELT_ID,
[DBA].US_SVO_NS_StoreOutItems.QTY_Released,
[DBA].US_SVO_NS_StoreOutItems.QTY_Restocked,
[DBA].US_SVO_NS_StoreOutItems.IDSOF as IDSOF_,
[DBA].US_SVO_NS_StoreOut.SOFdate as SOFdate_,
at2.RegistrationNumber,
[DBA].US_SVO_NS_StoreOutItems.IDProperty,
bum.SymbolInt,
[dba].US_SVO_NS_Store.PN,
[dba].US_SVO_NS_Store.SN,
StoreOutTransactions.TransactionType,
[DBA].US_SVO_NS_StoreOut.IDCustomer as IDCustomer_,
[dba].US_SVO_NS_Store.IDBalanceType,
[DBA].US_SVO_NS_Store.IDUM as IDum_
from [DBA].US_SVO_NS_StoreOutItems
join [DBA].US_SVO_NS_StoreOut on [DBA].US_SVO_NS_StoreOut.ID = [DBA].US_SVO_NS_StoreOutItems.IDSOF
left join [DBA].SOTransactionsCross on [DBA].SOTransactionsCross.IDStore = number_store and [DBA].SOTransactionsCross.IDSOF = [DBA].US_SVO_NS_StoreOut.ID
left join [DBA].StoreOutTransactions on [DBA].StoreOutTransactions.ID = [DBA].SOTransactionsCross.IDStoreOutTransaction
left join [DBA].US_SVO_NS_Store on [DBA].US_SVO_NS_Store.ELT_BN = [DBA].US_SVO_NS_StoreOutItems.ELT_BN and [DBA].US_SVO_NS_Store.ID = [DBA].US_SVO_NS_StoreOutItems.IDInStoreTable
left join [mma].BasUnMeas bum on bum.ID = US_SVO_NS_Store.IDUM
left join [dba].ACRegType at2 on at2.ID = US_SVO_NS_StoreOut.IDACReg
union
select
34 as number_store,
'VIRT_DME' as name_store,
[DBA].VIRT_DME_StoreOut.IDMJSS,
[DBA].VIRT_DME_StoreOutItems.id as id_,
[DBA].VIRT_DME_StoreOutItems.ELT_BN,
[DBA].VIRT_DME_Store.ELT_ID,
[DBA].VIRT_DME_StoreOutItems.QTY_Released,
[DBA].VIRT_DME_StoreOutItems.QTY_Restocked,
[DBA].VIRT_DME_StoreOutItems.IDSOF as IDSOF_,
[DBA].VIRT_DME_StoreOut.SOFdate as SOFdate_,
at2.RegistrationNumber,
[DBA].VIRT_DME_StoreOutItems.IDProperty,
bum.SymbolInt,
[dba].VIRT_DME_Store.PN,
[dba].VIRT_DME_Store.SN,
StoreOutTransactions.TransactionType,
[DBA].VIRT_DME_StoreOut.IDCustomer as IDCustomer_,
[dba].VIRT_DME_Store.IDBalanceType,
[DBA].VIRT_DME_Store.IDUM as IDum_
from [DBA].VIRT_DME_StoreOutItems
join [DBA].VIRT_DME_StoreOut on [DBA].VIRT_DME_StoreOut.ID = [DBA].VIRT_DME_StoreOutItems.IDSOF
left join [DBA].SOTransactionsCross on [DBA].SOTransactionsCross.IDStore = number_store and [DBA].SOTransactionsCross.IDSOF = [DBA].VIRT_DME_StoreOut.ID
left join [DBA].StoreOutTransactions on [DBA].StoreOutTransactions.ID = [DBA].SOTransactionsCross.IDStoreOutTransaction
left join [DBA].VIRT_DME_Store on [DBA].VIRT_DME_Store.ELT_BN = [DBA].VIRT_DME_StoreOutItems.ELT_BN and [DBA].VIRT_DME_Store.ID = [DBA].VIRT_DME_StoreOutItems.IDInStoreTable
left join [mma].BasUnMeas bum on bum.ID = VIRT_DME_Store.IDUM
left join [dba].ACRegType at2 on at2.ID = VIRT_DME_StoreOut.IDACReg
union
select
2 as number_store,
'VIRT_KJA' as name_store,
[DBA].VIRT_KJA_StoreOut.IDMJSS,
[DBA].VIRT_KJA_StoreOutItems.id as id_,
[DBA].VIRT_KJA_StoreOutItems.ELT_BN,
[DBA].VIRT_KJA_Store.ELT_ID,
[DBA].VIRT_KJA_StoreOutItems.QTY_Released,
[DBA].VIRT_KJA_StoreOutItems.QTY_Restocked,
[DBA].VIRT_KJA_StoreOutItems.IDSOF as IDSOF_,
[DBA].VIRT_KJA_StoreOut.SOFdate as SOFdate_,
at2.RegistrationNumber,
[DBA].VIRT_KJA_StoreOutItems.IDProperty,
bum.SymbolInt,
[dba].VIRT_KJA_Store.PN,
[dba].VIRT_KJA_Store.SN,
StoreOutTransactions.TransactionType,
[DBA].VIRT_KJA_StoreOut.IDCustomer as IDCustomer_,
[dba].VIRT_KJA_Store.IDBalanceType,
[DBA].VIRT_KJA_Store.IDUM as IDum_
from [DBA].VIRT_KJA_StoreOutItems
join [DBA].VIRT_KJA_StoreOut on [DBA].VIRT_KJA_StoreOut.ID = [DBA].VIRT_KJA_StoreOutItems.IDSOF
left join [DBA].SOTransactionsCross on [DBA].SOTransactionsCross.IDStore = number_store and [DBA].SOTransactionsCross.IDSOF = [DBA].VIRT_KJA_StoreOut.ID
left join [DBA].StoreOutTransactions on [DBA].StoreOutTransactions.ID = [DBA].SOTransactionsCross.IDStoreOutTransaction
left join [DBA].VIRT_KJA_Store on [DBA].VIRT_KJA_Store.ELT_BN = [DBA].VIRT_KJA_StoreOutItems.ELT_BN and [DBA].VIRT_KJA_Store.ID = [DBA].VIRT_KJA_StoreOutItems.IDInStoreTable
left join [mma].BasUnMeas bum on bum.ID = VIRT_KJA_Store.IDUM
left join [dba].ACRegType at2 on at2.ID = VIRT_KJA_StoreOut.IDACReg
)t2
)t_all
left join [DBA].MJSS on [DBA].MJSS.ID = t_all.idmjss
left join [DBA].MJSSType on [DBA].MJSSType.ID = [DBA].MJSS.IDMJSSType
left join [DBA].StoreBalanceType on [DBA].StoreBalanceType.Id = t_all.IDBalanceType
left join (
select p.PN as PN, CONVERT(nvarchar, p.KeyWordTranslation) as KeyWordTranslation, mc.Description, mc.Code, p1c.GUID1C
from DBA.PN p 
left join [DBA].PN1CGUID p1c on p.ID = p1c.IDPN and p1c.ERPName = '1CNS'
left join mma.MaterialClass mc on mc.ID = p.IDMCl
) pns on pns.PN = t_all.pn
left join (
SELECT IDCustomer, IDOperationType, IDMessage, IDStore, MessageOrder, max(MessageTime) as MessageTime, KSIPResponse, MessageText, KUPoLErrorText
FROM [DBA].ISAPMessageOrder
join (select max(imo.ID) as MssgTime, imo.IDMessage as IDMssg, imo.IDCustomer as IDCustomers from [DBA].ISAPMessageOrder imo GROUP BY IDMessage, IDCustomer) io 
on io.MssgTime = [DBA].ISAPMessageOrder.ID and io.IDMssg = [DBA].ISAPMessageOrder.IDMessage and io.IDCustomers = [DBA].ISAPMessageOrder.IDCustomer
WHERE IDOperationType = 3 and (KUPoLErrorText is not null or MessageText is not null)
GROUP BY IDCustomer, IDOperationType, IDMessage, IDStore, MessageOrder, KSIPResponse, KUPoLErrorText, MessageText
order by MessageTime desc
) errors on errors.idMessage = t_all.IDSOF_ and errors.IDStore = t_all.number_store and errors.IDCustomer = t_all.IDCustomer_
where cast(t_all.SOFdate_ as date) >= '2023-03-14'-- and t_all.PN = 'BACR12BU19SN'
group by 
t_all.name_store,
--t_all.id_,
cast(t_all.elt_bn as nvarchar),
cast(t_all.elt_id as nvarchar),
t_all.pn,
t_all.sn,
t_all.symbolint,
cast(t_all.idsof_ as nvarchar),
t_all.transactiontype ,
cast(t_all.sofdate_ as date),
t_all.registrationnumber,
t_all.IDPROPERTY,
[DBA].MJSS.MJSSNumber,
[DBA].MJSSType.MJSSType,
[DBA].StoreBalanceType.BalanceCode,
pns.Description, pns.KeyWordTranslation, pns.GUID1C,
errors.IDCustomer, errors.IDOperationType, errors.IDMessage, errors.IDStore, errors.MessageOrder, errors.MessageTime, errors.KSIPResponse, errors.MessageText, errors.KUPoLErrorText,
t_all.idcustomer_,
t_all.idum_,
case 
	when t_all.IDPROPERTY != '560' then 'Собственник не НордСтар!'
	when LENGTH(TRIM(t_all.ELT_ID))>0 /*and t_all.transactiontype != 'UTILIZATION'*/ then 'Инструмент'
	--when t_all.ELT_ID is not null and t_all.transactiontype != 'REPAIR' then 'Инструмент'
	when t_all.transactiontype != 'PRODUCTION' or t_all.transactiontype is not null then 'Тип SO не входит к отправке'
	when [DBA].StoreBalanceType.BalanceCode is null then 'Тип баланса не определен!'
	when [DBA].StoreBalanceType.BalanceCode != 'C' then 'Забаланс'
	else 'К отправке в 1С'
end,
case 
	when errors.KSIPResponse = '200' then 'Отправлен в 1С'
	when errors.KSIPResponse = '-200' then 'Ошибка отправки'
	when errors.KSIPResponse is null then 'Не отправлен'
	else null
end
        '''


	def get_1c_registr():
		return f'''
        select
case 
	when ptu_registr._Number is not null then 'Приобретение товаров и услуг ' + ptu_registr._Number
	when spis_registr._Number is not null then 'Списание на расходы ' + spis_registr._Number
 	when vozvrat_tovarov._Number is not null then 'Возврат товаров поставщику ' + vozvrat_tovarov._Number
	when peremestit._Number is not null then 'Перемещение товаров ' + peremestit._Number
	when storno_spis._Number is not null then 'Сторно списания на расходы ' + storno_spis._Number
	when peredacha._Number is not null then 'Передача переработчику ' + peredacha._Number
	when vozvrat_siria._Number is not null then 'Возврат от переработчика ' + vozvrat_siria._Number
	when sborka_razborka._Number is not null then 'Сборка (разборка) товаров ' + sborka_razborka._Number
	when realiazcia._Number is not null then 'Реализация товаров и услуг ' + realiazcia._Number
	when otvet_hranenie._Number is not null then 'Приемка товаров на хранение' + otvet_hranenie._Number
	when peredacha_hranitel._Number is not null then 'Передача на ответ хранение' + peredacha_hranitel._Number
	else registr_sebes._RecorderRRef
end as Registrator,
case	
	when ptu_registr._Number is not null then 'Приобретение товаров и услуг'
	when spis_registr._Number is not null then 'Списание на расходы'
 	when vozvrat_tovarov._Number is not null then 'Возврат товаров поставщику'
	when peremestit._Number is not null then 'Перемещение товаров'
	when storno_spis._Number is not null then 'Сторно списания на расходы'
	when peredacha._Number is not null then 'Передача переработчику'
	when vozvrat_siria._Number is not null then 'Возврат от переработчика'
	when sborka_razborka._Number is not null then 'Сборка (разборка) товаров'
	when realiazcia._Number is not null then 'Реализация товаров и услуг'
	when otvet_hranenie._Number is not null then 'Приемка товаров на хранение' 
	when peredacha_hranitel._Number is not null then 'Передача на ответ хранение'
	else registr_sebes._RecorderRRef 
end as Registrator_name,
case 
	when ptu_registr._Number is not null then ptu_registr._Number
	when spis_registr._Number is not null then spis_registr._Number
 	when vozvrat_tovarov._Number is not null then  vozvrat_tovarov._Number
	when peremestit._Number is not null then peremestit._Number
	when storno_spis._Number is not null then storno_spis._Number
	when peredacha._Number is not null then peredacha._Number
	when vozvrat_siria._Number is not null then vozvrat_siria._Number
	when sborka_razborka._Number is not null then sborka_razborka._Number
	when realiazcia._Number is not null then realiazcia._Number
	when otvet_hranenie._Number is not null then otvet_hranenie._Number
	when peredacha_hranitel._Number is not null then peredacha_hranitel._Number
	else registr_sebes._RecorderRRef
end as Registrator_number,
gtds.gtd_number as gtd_number,
/*iif(ptu._Number is not null, ptu._Number, 
iif(otvet_hranenie_partia._Number is not null, otvet_hranenie_partia._Number,
registr_sebes._Fld92745_RRRef))  as Partia,*/
cast(dateadd(year,-2000,registr_sebes._Period) as date) as date_doc,
nomenklatura.Nomen_code as Nomen_code,
nomenklatura.Nomen_name as Name,
monitor.SO_Number as SO_Number,
case 
	when monitor.elt_bn_ is null then seria.[_Description]
	else monitor.elt_bn_
end as Seria,
--seria.[_Description] as Seria,
--monitor.elt_bn_ as elt_bn_,
nomenklatura.Nomen_pn as PN,
sum(registr_sebes._Fld92749) as qty,
sum(iif(registr_sebes._RecordKind=1,registr_sebes._Fld92749*-1,registr_sebes._Fld92749)) as qty_kind,
sum(registr_sebes._Fld92760) as sum_,
iif(registr_sebes._RecordKind=1,'Списание','Поступление') as Status,
hoz_operacii.Синоним as Hoz_op,
orders._Description as order_,
IIF(object_rashod._Description is not null, object_rashod._Description, 
IIF(partners_analitika._Description is not null, partners_analitika._Description,
IIF(nd_analitika._Description is not null, nd_analitika._Description, 
registr_sebes._Fld92784_RRRef)))  as Analitika_rashodov,
right(IIF(object_rashod._Description is not null, object_rashod._Description, 
IIF(partners_analitika._Description is not null, partners_analitika._Description,
IIF(nd_analitika._Description is not null, nd_analitika._Description, 
registr_sebes._Fld92784_RRRef))),8) as registration_number,
partners._Description as Partner,
case 
	when cast(dateadd(year,-2000,registr_sebes._Period) as date) <= '2023-03-13' then 'Дата документа меньше, чем 14.03'
	else null
end as statusregistr_1c_so,
case 
	when users_ptu._Description is not null then users_ptu._Description
	when users_spis_registr._Description is not null then users_spis_registr._Description
	when users_vozvrat_tovarov._Description is not null then users_vozvrat_tovarov._Description
	when users_peremestit._Description is not null then users_peremestit._Description
	when users_storno_spis._Description is not null then users_storno_spis._Description
	when users_peredacha._Description is not null then users_peredacha._Description
	when users_vozvrat_siria._Description is not null then users_vozvrat_siria._Description
	when users_sborka_razborka._Description is not null then users_sborka_razborka._Description
	when users_realiazcia._Description is not null then users_realiazcia._Description
	when users_otvet_hranenie._Description is not null then users_otvet_hranenie._Description
	when users_peredacha_hranitel._Description is not null then users_peredacha_hranitel._Description
	else null
end as users
from _AccumRg92740 registr_sebes
left join _Document1540 ptu on ptu._IDRRef = registr_sebes._Fld92745_RRRef
left join _Document1527 otvet_hranenie_partia on otvet_hranenie_partia._IDRRef = registr_sebes._Fld92745_RRRef
left join _Document1540 ptu_registr on ptu_registr._IDRRef = registr_sebes._RecorderRRef
left join _Document1178 spis_registr on spis_registr._IDRRef = registr_sebes._RecorderRRef
left join _Reference452 analitik_nomen on analitik_nomen._IDRRef = registr_sebes._Fld92741RRef
left join _Reference848 orders on orders._IDRRef = analitik_nomen._Fld53262_RRRef
left join _Reference558 object_rashod on object_rashod._IDRRef = registr_sebes._Fld92784_RRRef
left join _Reference453 analitik_partia on analitik_partia._IDRRef = registr_sebes._Fld92746RRef
left join _Reference640 partners on partners._IDRRef = analitik_partia._Fld53274RRef
left join _Document1191 vozvrat_tovarov on vozvrat_tovarov._IDRRef = registr_sebes._RecorderRRef
left join _Document1475 peremestit on peremestit._IDRRef = registr_sebes._RecorderRRef
left join _Document1553 storno_spis on storno_spis._IDRRef = registr_sebes._RecorderRRef
left join _Document1461 peredacha on peredacha._IDRRef = registr_sebes._RecorderRRef
left join _Document1188 vozvrat_siria on vozvrat_siria._IDRRef = registr_sebes._RecorderRRef
left join _Document1601 sborka_razborka on sborka_razborka._IDRRef = registr_sebes._RecorderRRef
left join _Document1577 realiazcia on realiazcia._IDRRef = registr_sebes._RecorderRRef
left join _Reference640 partners_analitika on partners_analitika._IDRRef = registr_sebes._Fld92784_RRRef
left join _Reference508 nd_analitika on nd_analitika._IDRRef = registr_sebes._Fld92784_RRRef
left join _Document1527 otvet_hranenie on otvet_hranenie._IDRRef = registr_sebes._RecorderRRef
left join _Document1463 peredacha_hranitel on peredacha_hranitel._IDRRef = registr_sebes._RecorderRRef
left join ( --тут можно поставить left join, чтобы отключить проверку по наличию ГТД в регистре
select
gtd_tovar._Fld40328RRef as id_nomen,
gtd_tovar._Fld40346_RRRef as id_ptu,
LTRIM(RTRIM(gtd._Fld40297)) as gtd_number
from _Document1657 gtd
join _Document1657_VT40325 gtd_tovar on gtd_tovar._Document1657_IDRRef = gtd._IDRRef
where iif(_Posted='',1,0) = 0
) gtds on gtds.id_ptu = registr_sebes._Fld92745_RRRef and gtds.id_nomen = analitik_nomen._Fld53259RRef
left join (select
t1.IDnomen as IDnomen,
t1.Код as Nomen_Code,
t1.[Наименование] as Nomen_name,
t1.[Партийный номер (Сырье и материалы 10 01 ТД)] as Nomen_pn
from (
select *
from (
select
	_Reference539._IDRRef as IDnomen
	,IIF(_Reference539._Marked<>'','Удалено','Не_удалено') as ПометкаУдаления
	,_Reference539._Code as Код
	,_Fld55631 as Артикул
	,_Reference290._Description as ГруппаДоступа
	,_Reference539._Description as Наименование
	,_Reference221._Description as ВидНоменклатуры
	,_Chrc3194._Description as name_
	,_Fld55734_S as value
from dbo._Reference539
join dbo._Reference539_VT55731 on dbo._Reference539_VT55731._Reference539_IDRRef = dbo._Reference539._IDRRef
join dbo._Chrc3194 on dbo._Chrc3194._IDRRef = dbo._Reference539_VT55731._Fld55733RRef
left join dbo._Reference290 on dbo._Reference290._IDRRef = _Fld55642RRef
left join dbo._Reference221 on dbo._Reference221._IDRRef = _Fld55641RRef
left join dbo._InfoRg87665 on dbo._InfoRg87665._Fld87667RRef = dbo._Reference539.[_IDRRef] 
) src
pivot (max([value]) for [name_] in ([Код АСУ НСИ],[Guid КУПОЛ],[Партийный номер (Сырье и материалы 10 01 ТД)],[Тип номенклатуры (Сырье и материалы 10 01 ТД)])) as pvt
)t1
where t1.[Партийный номер (Сырье и материалы 10 01 ТД)] is not null
)nomenklatura on nomenklatura.IDnomen = analitik_nomen._Fld53259RRef
left join _Reference836 seria on analitik_nomen._Fld53261RRef = seria.[_IDRRef]
left join _Reference701 users_ptu on users_ptu._IDRRef = ptu_registr._Fld33129RRef
left join _Reference701 users_spis_registr on users_spis_registr._IDRRef = spis_registr._Fld9185RRef
left join _Reference701 users_vozvrat_tovarov on users_vozvrat_tovarov._IDRRef = vozvrat_tovarov._Fld10003RRef
left join _Reference701 users_peremestit on users_peremestit._IDRRef = peremestit._Fld29148RRef
left join _Reference701 users_storno_spis on users_storno_spis._IDRRef = storno_spis._Fld34602RRef
left join _Reference701 users_peredacha on users_peredacha._IDRRef = peredacha._Fld28475RRef
left join _Reference701 users_vozvrat_siria on users_vozvrat_siria._IDRRef = vozvrat_siria._Fld9631RRef
left join _Reference701 users_sborka_razborka on users_sborka_razborka._IDRRef = sborka_razborka._Fld37175RRef
left join _Reference701 users_realiazcia on users_realiazcia._IDRRef = realiazcia._Fld35985RRef
left join _Reference701 users_otvet_hranenie on users_otvet_hranenie._IDRRef = otvet_hranenie._Fld32303RRef
left join _Reference701 users_peredacha_hranitel on users_peredacha_hranitel._IDRRef = peredacha_hranitel._Fld28723RRef
left join (select
	_IDRRef as _IDRRef
	,_EnumOrder as Порядок
	,Имя
	,Синоним
from dbo._Enum3172
left join (
	select
		417 as N
		,N'ПередачаВЭксплуатацию' as Имя
		,N'Передача в эксплуатацию' as Синоним
) S on S.N=_Enum3172._EnumOrder
) hoz_operacii_spis on hoz_operacii_spis._IDRRef = spis_registr._Fld9173RRef
left join (select
	_IDRRef as _IDRRef
	,_EnumOrder as Порядок
	,Имя
	,Синоним
from dbo._Enum3172
left join (
	select
		0 as N
		,N'АвансовыйОтчет' as Имя
		,N'Авансовый отчет' as Синоним
	union all select
		1 as N
		,N'АмортизацияВнеоборотныхАктивов' as Имя
		,N'Амортизация внеоборотных активов' as Синоним
	union all select
		2 as N
		,N'АмортизацияНМА' as Имя
		,N'Амортизация НМА' as Синоним
	union all select
		3 as N
		,N'АмортизацияНМАвДругуюОрганизацию' as Имя
		,N'Амортизация НМА в другую организацию' as Синоним
	union all select
		4 as N
		,N'АмортизацияНМАизДругойОрганизации' as Имя
		,N'Амортизация НМА из другой организации' as Синоним
	union all select
		5 as N
		,N'АмортизацияОС' as Имя
		,N'Амортизация ОС' as Синоним
	union all select
		6 as N
		,N'АмортизацияОСвДругуюОрганизацию' as Имя
		,N'Амортизация ОС в другую организацию' as Синоним
	union all select
		7 as N
		,N'АмортизацияОСизДругойОрганизации' as Имя
		,N'Амортизация ОС из другой организации' as Синоним
	union all select
		8 as N
		,N'АннулированиеПодарочныхСертификатов' as Имя
		,N'Аннулирование подарочных сертификатов' as Синоним
	union all select
		9 as N
		,N'БронированиеУПоставщика' as Имя
		,N'Бронирование у поставщика' as Синоним
	union all select
		10 as N
		,N'БронированиеЧерезАгента' as Имя
		,N'Бронирование через агента' as Синоним
	union all select
		11 as N
		,N'БронированиеЧерезПодотчетноеЛицо' as Имя
		,N'Бронирование через подотчетное лицо' as Синоним
	union all select
		12 as N
		,N'ВводДанныхПоНалогуНаПрибыль' as Имя
		,N'Ввод данных по налогу на прибыль' as Синоним
	union all select
		13 as N
		,N'ВводИнформацииОПрошлыхРемонтах' as Имя
		,N'Ввод информации о прошлых ремонтах' as Синоним
	union all select
		14 as N
		,N'ВводОстатковАвансовКлиентов' as Имя
		,N'Ввод остатков авансов клиентов' as Синоним
	union all select
		15 as N
		,N'ВводОстатковАвансовПоставщикам' as Имя
		,N'Ввод остатков авансов поставщикам' as Синоним
	union all select
		16 as N
		,N'ВводОстатковАмортизацииНМАиРасходовНаНИОКР' as Имя
		,N'Ввод остатков амортизации НМА и расходов на НИОКР' as Синоним
	union all select
		17 as N
		,N'ВводОстатковАмортизацииОС' as Имя
		,N'Ввод остатков амортизации ОС' as Синоним
	union all select
		18 as N
		,N'ВводОстатковАрендованныхОСЗаБалансом' as Имя
		,N'Ввод остатков арендованных ОС (за балансом)' as Синоним
	union all select
		19 as N
		,N'ВводОстатковАрендованныхОСНаБалансе' as Имя
		,N'Ввод остатков арендованных ОС (на балансе)' as Синоним
	union all select
		20 as N
		,N'ВводОстатковВАвтономныхКассахККМКОформлениюОтчетовОРозничныхПродажах' as Имя
		,N'Ввод остатков в автономных кассах ККМ к оформлению отчетов о розничных продажах' as Синоним
	union all select
		21 as N
		,N'ВводОстатковВАвтономныхКассахККМПоРозничнойВыручке' as Имя
		,N'Ввод остатков в автономных кассах ККМ по розничной выручке' as Синоним
	union all select
		22 as N
		,N'ВводОстатковВзаиморасчетовПоДоговорамАренды' as Имя
		,N'Ввод остатков взаиморасчетов по договорам аренды' as Синоним
	union all select
		23 as N
		,N'ВводОстатковВКассах' as Имя
		,N'Ввод остатков в кассах' as Синоним
	union all select
		24 as N
		,N'ВводОстатковВложенийВоВнеоборотныеАктивы' as Имя
		,N'Ввод остатков вложений во внеоборотные активы' as Синоним
	union all select
		25 as N
		,N'ВводОстатковВозвратнойТарыПереданнойКлиентам' as Имя
		,N'Ввод остатков возвратной тары переданной клиентам' as Синоним
	union all select
		26 as N
		,N'ВводОстатковВозвратнойТарыПринятойОтПоставщиков' as Имя
		,N'Ввод остатков возвратной тары принятой от поставщиков' as Синоним
	union all select
		27 as N
		,N'ВводОстатковДенежныхСредствКПоступлениюОтЭквайера' as Имя
		,N'Ввод остатков денежных средств к поступлению от эквайера' as Синоним
	union all select
		28 as N
		,N'ВводОстатковЗадолженностиКлиентов' as Имя
		,N'Ввод остатков задолженности клиентов' as Синоним
	union all select
		29 as N
		,N'ВводОстатковЗадолженностиПодотчетников' as Имя
		,N'Ввод остатков задолженности подотчетников' as Синоним
	union all select
		30 as N
		,N'ВводОстатковЗадолженностиПоставщикам' as Имя
		,N'Ввод остатков задолженности поставщикам' as Синоним
	union all select
		31 as N
		,N'ВводОстатковЗатратПартийПроизводства' as Имя
		,N'Ввод остатков затрат партий производства' as Синоним
	union all select
		32 as N
		,N'ВводОстатковМатериаловПереданныхВПроизводство' as Имя
		,N'Ввод остатков материалов, переданных в производство' as Синоним
	union all select
		33 as N
		,N'ВводОстатковМатериаловПереданныхПереработчикам' as Имя
		,N'Ввод остатков материалов, переданных переработчикам (2.4)' as Синоним
	union all select
		34 as N
		,N'ВводОстатковМатериаловПереданныхПереработчикам2_5' as Имя
		,N'Ввод остатков материалов, переданных переработчикам' as Синоним
	union all select
		35 as N
		,N'ВводОстатковМатериаловПринятыхВПереработку2_5' as Имя
		,N'Ввод остатков материалов, принятых в переработку' as Синоним
	union all select
		36 as N
		,N'ВводОстатковНаБанковскихСчетах' as Имя
		,N'Ввод остатков на банковских счетах' as Синоним
	union all select
		37 as N
		,N'ВводОстатковНДСПоПриобретеннымЦенностям' as Имя
		,N'Ввод остатков НДС по приобретенным ценностям' as Синоним
	union all select
		38 as N
		,N'ВводОстатковНМАиРасходовНаНИОКР' as Имя
		,N'Ввод остатков нематериальных активов и расходов на НИОКР' as Синоним
	union all select
		39 as N
		,N'ВводОстатковОбесцененияМатериаловПереданныхВПроизводство' as Имя
		,N'Ввод остатков обесценения материалов переданных в производство' as Синоним
	union all select
		40 as N
		,N'ВводОстатковОбесцененияМатериаловПереданныхПереработчикам' as Имя
		,N'Ввод остатков обесценения материалов переданных переработчикам' as Синоним
	union all select
		41 as N
		,N'ВводОстатковОбесцененияНМА' as Имя
		,N'Ввод остатков обесценения НМА' as Синоним
	union all select
		42 as N
		,N'ВводОстатковОбесцененияОС' as Имя
		,N'Ввод остатков обесценения ОС' as Синоним
	union all select
		43 as N
		,N'ВводОстатковОбесцененияСобственныхТоваров' as Имя
		,N'Ввод остатков обесценения собственных товаров' as Синоним
	union all select
		44 as N
		,N'ВводОстатковОбесцененияТоваровПереданныхНаКомиссию' as Имя
		,N'Ввод остатков обесценения товаров переданных на комиссию' as Синоним
	union all select
		45 as N
		,N'ВводОстатковОптовыхПродажЗаПрошлыеПериоды' as Имя
		,N'Ввод остатков оптовых продаж за прошлые периоды' as Синоним
	union all select
		46 as N
		,N'ВводОстатковОсновныхСредств' as Имя
		,N'Ввод остатков основных средств' as Синоним
	union all select
		47 as N
		,N'ВводОстатковПереданныхВАрендуОС' as Имя
		,N'Ввод остатков переданных в аренду основных средств' as Синоним
	union all select
		48 as N
		,N'ВводОстатковПереданныхВАрендуПредметовЛизингаНаБалансе' as Имя
		,N'Ввод остатков переданных в аренду предметов лизинга на балансе' as Синоним
	union all select
		49 as N
		,N'ВводОстатковПерерасходовПодотчетныхСредств' as Имя
		,N'Ввод остатков перерасходов подотчетных средств' as Синоним
	union all select
		50 as N
		,N'ВводОстатковПодарочныхСертификатов' as Имя
		,N'Ввод остатков подарочных сертификатов' as Синоним
	union all select
		51 as N
		,N'ВводОстатковПоДоговорамКредитовИДепозитов' as Имя
		,N'Ввод остатков по договорам кредитов и депозитов' as Синоним
	union all select
		52 as N
		,N'ВводОстатковПолуфабрикатовДавальца2_5' as Имя
		,N'Ввод остатков полуфабрикатов давальца' as Синоним
	union all select
		53 as N
		,N'ВводОстатковПредметовЛизингаЗаБалансом' as Имя
		,N'Ввод остатков предметов лизинга за балансом' as Синоним
	union all select
		54 as N
		,N'ВводОстатковПриПереходеНаИспользованиеАдресногоХраненияОстатков' as Имя
		,N'Ввод остатков при переходе на использование адресного хранения остатков' as Синоним
	union all select
		55 as N
		,N'ВводОстатковПриПереходеНаИспользованиеСкладскихПомещений' as Имя
		,N'Ввод остатков при переходе на использование складских помещений' as Синоним
	union all select
		56 as N
		,N'ВводОстатковПродукцииДавальца2_5' as Имя
		,N'Ввод остатков продукции давальца' as Синоним
	union all select
		57 as N
		,N'ВводОстатковПрочихАктивовПассивов' as Имя
		,N'Ввод остатков прочих активов пассивов' as Синоним
	union all select
		58 as N
		,N'ВводОстатковПрочихРасходов' as Имя
		,N'Ввод остатков прочих расходов' as Синоним
	union all select
		59 as N
		,N'ВводОстатковПрочихРасходовУСН' as Имя
		,N'Ввод остатков прочих расходов УСН' as Синоним
	union all select
		60 as N
		,N'ВводОстатковРасходовУСНПоМатериалам' as Имя
		,N'Ввод остатков расходов УСН по материалам' as Синоним
	union all select
		61 as N
		,N'ВводОстатковРасходовУСНПоТоварам' as Имя
		,N'Ввод остатков расходов УСН по товарам' as Синоним
	union all select
		62 as N
		,N'ВводОстатковРасчетовМеждуОрганизациямиПоАвансам' as Имя
		,N'Ввод остатков расчетов между организациями по авансам' as Синоним
	union all select
		63 as N
		,N'ВводОстатковРасчетовМеждуОрганизациямиПоРеализациям' as Имя
		,N'Ввод остатков расчетов между организациями по реализациям' as Синоним
	union all select
		64 as N
		,N'ВводОстатковРемонтов' as Имя
		,N'Ввод остатков ремонтов' as Синоним
	union all select
		65 as N
		,N'ВводОстатковРозничныхПродажЗаПрошлыеПериоды' as Имя
		,N'Ввод остатков розничных продаж за прошлые периоды' as Синоним
	union all select
		66 as N
		,N'ВводОстатковСобственныхТоваров' as Имя
		,N'Ввод остатков собственных товаров' as Синоним
	union all select
		67 as N
		,N'ВводОстатковСтоимостиНМАиРасходовНаНИОКР' as Имя
		,N'Ввод остатков стоимости НМА и расходов на НИОКР' as Синоним
	union all select
		68 as N
		,N'ВводОстатковСтоимостиОС' as Имя
		,N'Ввод остатков стоимости ОС' as Синоним
	union all select
		69 as N
		,N'ВводОстатковТМЦВЭксплуатации' as Имя
		,N'Ввод остатков ТМЦ в эксплуатации' as Синоним
	union all select
		70 as N
		,N'ВводОстатковТоваровПереданныхНаКомиссию' as Имя
		,N'Ввод остатков товаров, переданных на комиссию' as Синоним
	union all select
		71 as N
		,N'ВводОстатковТоваровПолученныхНаКомиссию' as Имя
		,N'Ввод остатков товаров, полученных на комиссию' as Синоним
	union all select
		72 as N
		,N'ВводОстатковФинансовогоРезультатаЗаПрошлыеПериоды' as Имя
		,N'Ввод остатков финансового результата за прошлые периоды' as Синоним
	union all select
		73 as N
		,N'ВводПервоначальныхСведенийДляРасчетаЗемельногоНалога' as Имя
		,N'Ввод первоначальных сведений для расчета земельного налога' as Синоним
	union all select
		74 as N
		,N'ВводПервоначальныхСведенийДляРасчетаНалогаНаИмущество' as Имя
		,N'Ввод первоначальных сведений для расчета налога на имущество' as Синоним
	union all select
		75 as N
		,N'ВводПервоначальныхСведенийДляРасчетаТранспортногоНалога' as Имя
		,N'Ввод первоначальных сведений для расчета транспортного налога' as Синоним
	union all select
		76 as N
		,N'ВзаимозачетДебиторскойЗадолженности' as Имя
		,N'Взаимозачет дебиторской задолженности' as Синоним
	union all select
		77 as N
		,N'ВзаимозачетЗадолженности' as Имя
		,N'Взаимозачет задолженности' as Синоним
	union all select
		78 as N
		,N'ВзаимозачетКредиторскойЗадолженности' as Имя
		,N'Взаимозачет кредиторской задолженности' as Синоним
	union all select
		79 as N
		,N'ВключениеАмортизационнойПремииВРасходы' as Имя
		,N'Включение амортизационной премии в расходы' as Синоним
	union all select
		80 as N
		,N'ВключениеИсключениеНДСВСтоимости' as Имя
		,N'Включение/исключение НДС в стоимости' as Синоним
	union all select
		81 as N
		,N'ВключениеНДСВСтоимость' as Имя
		,N'Включение НДС в стоимость' as Синоним
	union all select
		82 as N
		,N'ВнесениеДенежныхСредствВКассуККМ' as Имя
		,N'Внесение ДС в кассу ККМ' as Синоним
	union all select
		83 as N
		,N'ВнутреннееПоступлениеДенежныхСредств' as Имя
		,N'Внутреннее поступление ДС' as Синоним
	union all select
		84 as N
		,N'ВнутреннееПоступлениеРабот' as Имя
		,N'Внутреннее поступление работ' as Синоним
	union all select
		85 as N
		,N'ВнутреннееПоступлениеРасходов' as Имя
		,N'Внутреннее поступление расходов' as Синоним
	union all select
		86 as N
		,N'ВнутреннееПоступлениеТоваров' as Имя
		,N'Внутреннее поступление товаров' as Синоним
	union all select
		87 as N
		,N'ВнутреннееПотребление' as Имя
		,N'Внутреннее потребление' as Синоним
	union all select
		88 as N
		,N'ВнутренняяПередачаДенежныхСредств' as Имя
		,N'Передача ДС между организацией и филиалами' as Синоним
	union all select
		89 as N
		,N'ВозвратБронирования' as Имя
		,N'Возврат бронирования' as Синоним
	union all select
		90 as N
		,N'ВозвратБронированияПодотчетногоЛица' as Имя
		,N'Возврат бронирования подотчетного лица' as Синоним
	union all select
		91 as N
		,N'ВозвратВыкупнойСтоимостиПредметовАренды' as Имя
		,N'Возврат выкупной стоимости предметов аренды' as Синоним
	union all select
		92 as N
		,N'ВозвратВыкупнойСтоимостиПредметовАрендыАванс' as Имя
		,N'Возврат выкупной стоимости предметов аренды (аванс)' as Синоним
	union all select
		93 as N
		,N'ВозвратДавальцу' as Имя
		,N'Возврат давальцу (2.4)' as Синоним
	union all select
		94 as N
		,N'ВозвратДавальцу2_5' as Имя
		,N'Возврат давальцу' as Синоним
	union all select
		95 as N
		,N'ВозвратДенежныхДокументовПоставщику' as Имя
		,N'Возврат денежных документов поставщику' as Синоним
	union all select
		96 as N
		,N'ВозвратДенежныхСредствВДругуюОрганизацию' as Имя
		,N'Возврат ДС другой организации' as Синоним
	union all select
		97 as N
		,N'ВозвратДенежныхСредствОтАрендодателя' as Имя
		,N'Возврат ДС от арендодателя' as Синоним
	union all select
		98 as N
		,N'ВозвратДенежныхСредствОтДругойОрганизации' as Имя
		,N'Возврат ДС от другой организации' as Синоним
	union all select
		99 as N
		,N'ВозвратДенежныхСредствОтПодотчетника' as Имя
		,N'Возврат ДС от подотчетника' as Синоним
	union all select
		100 as N
		,N'ВозвратДенежныхСредствОтПоставщика' as Имя
		,N'Возврат ДС от поставщика' as Синоним
	union all select
		101 as N
		,N'ВозвратДеньВДень' as Имя
		,N'Возврат день в день' as Синоним
	union all select
		102 as N
		,N'ВозвратИзПроизводства' as Имя
		,N'Возврат из производства' as Синоним
	union all select
		103 as N
		,N'ВозвратИзЭксплуатации' as Имя
		,N'Возврат из эксплуатации' as Синоним
	union all select
		104 as N
		,N'ВозвратМатериаловИзКладовой' as Имя
		,N'Возврат материалов из кладовой' as Синоним
	union all select
		105 as N
		,N'ВозвратМатериаловИзПроизводства' as Имя
		,N'Возврат материалов из производства' as Синоним
	union all select
		106 as N
		,N'ВозвратНалогов' as Имя
		,N'Возврат налогов' as Синоним
	union all select
		107 as N
		,N'ВозвратНедопоставленногоТовара' as Имя
		,N'Возврат недопоставленного товара' as Синоним
	union all select
		108 as N
		,N'ВозвратНеперечисленнойЗарплатыПоЗарплатномуПроекту' as Имя
		,N'Возврат по зарплатному проекту' as Синоним
	union all select
		109 as N
		,N'ВозвратНеперечисленныхДС' as Имя
		,N'Возврат неперечисленной зарплаты на лицевые счета' as Синоним
	union all select
		110 as N
		,N'ВозвратОбеспечительногоПлатежа' as Имя
		,N'Возврат обеспечительного платежа' as Синоним
	union all select
		111 as N
		,N'ВозвратОплатыКлиенту' as Имя
		,N'Возврат оплаты клиенту' as Синоним
	union all select
		112 as N
		,N'ВозвратОплатыКлиентуНаПлатежнуюКарту' as Имя
		,N'Возврат оплаты клиенту на платежную карту' as Синоним
	union all select
		113 as N
		,N'ВозвратОплатыКомиссионеру' as Имя
		,N'Возврат оплаты комиссионеру' as Синоним
	union all select
		114 as N
		,N'ВозвратОплатыНаПлатежнуюКарту' as Имя
		,N'Возврат оплаты по эквайрингу' as Синоним
	union all select
		115 as N
		,N'ВозвратОСИзАренды' as Имя
		,N'Возврат ОС из аренды' as Синоним
	union all select
		116 as N
		,N'ВозвратОтКомиссионера' as Имя
		,N'Возврат от комиссионера' as Синоним
	union all select
		117 as N
		,N'ВозвратОтПереработчика' as Имя
		,N'Возврат от переработчика (2.4)' as Синоним
	union all select
		118 as N
		,N'ВозвратОтПереработчика2_5' as Имя
		,N'Возврат от переработчика' as Синоним
	union all select
		119 as N
		,N'ВозвратОтРозничногоПокупателя' as Имя
		,N'Возврат от розничного покупателя' as Синоним
	union all select
		120 as N
		,N'ВозвратОтХранителя' as Имя
		,N'Возврат от хранителя' as Синоним
	union all select
		121 as N
		,N'ВозвратПодарочныхСертификатов' as Имя
		,N'Возврат подарочных сертификатов' as Синоним
	union all select
		122 as N
		,N'ВозвратПоКомиссииМеждуОрганизациями' as Имя
		,N'Возврат по комиссии между организациями' as Синоним
	union all select
		123 as N
		,N'ВозвратТарыОтКлиентаПрошлыхПериодов' as Имя
		,N'Возврат тары от клиента прошлых периодов' as Синоним
	union all select
		124 as N
		,N'ВозвратТоваровКомитенту' as Имя
		,N'Возврат товаров комитенту' as Синоним
	union all select
		125 as N
		,N'ВозвратТоваровМеждуОрганизациями' as Имя
		,N'Возврат товаров между организациями' as Синоним
	union all select
		126 as N
		,N'ВозвратТоваровОтКлиента' as Имя
		,N'Возврат товаров от клиента' as Синоним
	union all select
		127 as N
		,N'ВозвратТоваровОтКлиентаПрошлыхПериодов' as Имя
		,N'Возврат товаров от клиента прошлых периодов' as Синоним
	union all select
		128 as N
		,N'ВозвратТоваровПоставщику' as Имя
		,N'Возврат товаров поставщику' as Синоним
	union all select
		129 as N
		,N'ВозвратТоваровЧерезКомиссионера' as Имя
		,N'Возврат товаров через комиссионера' as Синоним
	union all select
		130 as N
		,N'ВозвратТоваровЧерезКомиссионераПрошлыхПериодов' as Имя
		,N'Возврат товаров через комиссионера прошлых периодов' as Синоним
	union all select
		131 as N
		,N'ВосстановлениеАвансаКлиента' as Имя
		,N'Восстановление аванса клиента' as Синоним
	union all select
		132 as N
		,N'ВосстановлениеАвансаПоставщику' as Имя
		,N'Восстановление аванса поставщику' as Синоним
	union all select
		133 as N
		,N'ВосстановлениеАмортизационнойПремии' as Имя
		,N'Восстановление амортизационной премии' as Синоним
	union all select
		134 as N
		,N'ВосстановлениеДолгаКлиента' as Имя
		,N'Восстановление долга клиента' as Синоним
	union all select
		135 as N
		,N'ВосстановлениеДолгаПоставщику' as Имя
		,N'Восстановление долга поставщику' as Синоним
	union all select
		136 as N
		,N'ВосстановлениеНДС' as Имя
		,N'Восстановление НДС' as Синоним
	union all select
		137 as N
		,N'ВосстановлениеНДССВыданногоАванса' as Имя
		,N'Восстановление НДС с выданного аванса' as Синоним
	union all select
		138 as N
		,N'ВосстановлениеОбесцененияНМА' as Имя
		,N'Восстановление обесценения НМА' as Синоним
	union all select
		139 as N
		,N'ВосстановлениеОбесцененияОС' as Имя
		,N'Восстановление обесценения ОС' as Синоним
	union all select
		140 as N
		,N'ВосстановлениеРезервовПоСомнительнымДолгам' as Имя
		,N'Восстановление резервов по сомнительным долгам' as Синоним
	union all select
		141 as N
		,N'ВходящийНДСПоПриобретению' as Имя
		,N'Входящий НДС по приобретению' as Синоним
	union all select
		142 as N
		,N'ВыбытиеАрендованныхОС' as Имя
		,N'Выбытие арендованных ОС (забалансовый учет)' as Синоним
	union all select
		143 as N
		,N'ВыдачаДенежныхДокументовПодотчетнику' as Имя
		,N'Выдача денежных документов подотчетному лицу' as Синоним
	union all select
		144 as N
		,N'ВыдачаДенежныхСредствВДругуюКассу' as Имя
		,N'Выдача ДС в другую кассу' as Синоним
	union all select
		145 as N
		,N'ВыдачаДенежныхСредствВКассуККМ' as Имя
		,N'Выдача ДС в кассу ККМ' as Синоним
	union all select
		146 as N
		,N'ВыдачаДенежныхСредствПодотчетнику' as Имя
		,N'Выдача ДС подотчетнику' as Синоним
	union all select
		147 as N
		,N'ВыдачаЗаймаСотруднику' as Имя
		,N'Выдача займа сотруднику' as Синоним
	union all select
		148 as N
		,N'ВыдачаЗаймов' as Имя
		,N'Выдача займа контрагенту' as Синоним
	union all select
		149 as N
		,N'ВыделениеАмортизацииОСПриРазукомплектации' as Имя
		,N'Выделение амортизации ОС при разукомплектации' as Синоним
	union all select
		150 as N
		,N'ВыделениеСтоимостиОСПриРазукомплектации' as Имя
		,N'Выделение стоимости ОС при разукомплектации' as Синоним
	union all select
		151 as N
		,N'ВыделениеУзловКомпонентовАмортизации' as Имя
		,N'Выделение узлов и компонентов амортизации' as Синоним
	union all select
		152 as N
		,N'ВыемкаДенежныхСредствИзКассыККМ' as Имя
		,N'Выемка ДС из кассы ККМ' as Синоним
	union all select
		153 as N
		,N'ВыкупАрендованныхОС' as Имя
		,N'Выкуп арендованных ОС' as Синоним
	union all select
		154 as N
		,N'ВыкупВозвратнойТарыКлиентом' as Имя
		,N'Выкуп возвратной тары клиентом' as Синоним
	union all select
		155 as N
		,N'ВыкупПринятыхНаХранениеТоваров' as Имя
		,N'Выкуп товаров с хранения' as Синоним
	union all select
		156 as N
		,N'ВыкупТоваровДавальца' as Имя
		,N'Выкуп товаров давальца' as Синоним
	union all select
		157 as N
		,N'ВыкупТоваровПереданныхВПроизводство' as Имя
		,N'Выкуп товаров, переданных в производство' as Синоним
	union all select
		158 as N
		,N'ВыкупТоваровПереданныхНаХранение' as Имя
		,N'Выкуп товаров, переданных на хранение' as Синоним
	union all select
		159 as N
		,N'ВыкупТоваровПереработчиком' as Имя
		,N'Выкуп товаров переработчиком' as Синоним
	union all select
		160 as N
		,N'ВыкупТоваровХранителем' as Имя
		,N'Выкуп товаров хранителем' as Синоним
	union all select
		161 as N
		,N'ВыплатаЗарплаты' as Имя
		,N'Выплата по ведомости' as Синоним
	union all select
		162 as N
		,N'ВыплатаЗарплатыНаЛицевыеСчета' as Имя
		,N'Выплата по ведомости на лицевые счета' as Синоним
	union all select
		163 as N
		,N'ВыплатаЗарплатыПоЗарплатномуПроекту' as Имя
		,N'Выплата по ведомости по зарплатному проекту' as Синоним
	union all select
		164 as N
		,N'ВыплатаЗарплатыРаботнику' as Имя
		,N'Выплата по ведомости работнику' as Синоним
	union all select
		165 as N
		,N'ВыплатаЗарплатыРаздатчиком' as Имя
		,N'Выплата по ведомости раздатчиком' as Синоним
	union all select
		166 as N
		,N'ВыплатаЗарплатыЧерезКассу' as Имя
		,N'Выплата по ведомости через кассу' as Синоним
	union all select
		167 as N
		,N'ВыпускПродукции' as Имя
		,N'Выпуск продукции' as Синоним
	union all select
		168 as N
		,N'ВыпускПродукцииВПодразделение' as Имя
		,N'Выпуск продукции в подразделение' as Синоним
	union all select
		169 as N
		,N'ВыпускПродукцииНаСклад' as Имя
		,N'Выпуск продукции на склад' as Синоним
	union all select
		170 as N
		,N'ВыпускПродукцииПостатейные' as Имя
		,N'Выпуск продукции (постатейные)' as Синоним
	union all select
		171 as N
		,N'ВыпускПродукцииТрудозатраты' as Имя
		,N'Выпуск продукции (трудозатраты)' as Синоним
	union all select
		172 as N
		,N'ВыпускПродукцииФиксированнаяСтоимость' as Имя
		,N'Выпуск продукции (фикс. стоимость)' as Синоним
	union all select
		173 as N
		,N'ВыработкаНМА' as Имя
		,N'Выработка НМА' as Синоним
	union all select
		174 as N
		,N'ВычетНДССВыданногоАванса' as Имя
		,N'Вычет НДС с выданного аванса' as Синоним
	union all select
		175 as N
		,N'ВычетНДССПолученногоАванса' as Имя
		,N'Вычет НДС с полученного аванса' as Синоним
	union all select
		176 as N
		,N'ДвижениеАктивовПассивовЗаСчетАктивовПассивов' as Имя
		,N'Движение активов/пассивов за счет активов/пассивов' as Синоним
	union all select
		177 as N
		,N'ДвижениеДоходовЗаСчетАктивовПассивов' as Имя
		,N'Движение доходов за счет активов/пассивов' as Синоним
	union all select
		178 as N
		,N'ДвижениеДоходовЗаСчетРасходов' as Имя
		,N'Движение доходов за счет расходов' as Синоним
	union all select
		179 as N
		,N'ДвижениеРасходовЗаСчетАктивовПассивов' as Имя
		,N'Движение расходов за счет активов/пассивов' as Синоним
	union all select
		180 as N
		,N'ДвижениеРасходовЗаСчетДоходов' as Имя
		,N'Движение расходов за счет доходов' as Синоним
	union all select
		181 as N
		,N'ДепонированиеЗарплаты' as Имя
		,N'Депонирование зарплаты' as Синоним
	union all select
		182 as N
		,N'ДоначислениеЗемельногоНалога' as Имя
		,N'Доначисление земельного налога' as Синоним
	union all select
		183 as N
		,N'ДоначислениеНалогаНаИмущество' as Имя
		,N'Доначисление налога на имущество' as Синоним
	union all select
		184 as N
		,N'ДоначислениеТранспортногоНалога' as Имя
		,N'Доначисление транспортного налога' as Синоним
	union all select
		185 as N
		,N'ДополнительныеРасходыБезПартии' as Имя
		,N'Дополнительные расходы без указания документа партии' as Синоним
	union all select
		186 as N
		,N'ДополнительныеРасходыСПартией' as Имя
		,N'Дополнительные расходы с указанием документа партии' as Синоним
	union all select
		187 as N
		,N'ДосрочноеПрекращениеДоговораАренды' as Имя
		,N'Досрочное прекращение договора аренды' as Синоним
	union all select
		188 as N
		,N'ДосрочныйВыкупАрендованныхОС' as Имя
		,N'Досрочный выкуп арендованных ОС' as Синоним
	union all select
		189 as N
		,N'ДоходыОтПереоценкиТоваров' as Имя
		,N'Доходы от переоценки товаров' as Синоним
	union all select
		190 as N
		,N'ДоходыПоОтчетуКомиссионераОСписании' as Имя
		,N'Доходы по отчету комиссионера о списании' as Синоним
	union all select
		191 as N
		,N'ЗавершениеЭтаповИсследованийИРазработок' as Имя
		,N'Завершение этапов исследований и разработок' as Синоним
	union all select
		192 as N
		,N'ЗаключениеДоговораАренды' as Имя
		,N'Заключение договора аренды' as Синоним
	union all select
		193 as N
		,N'ЗакрытиеМесяца' as Имя
		,N'Закрытие месяца' as Синоним
	union all select
		194 as N
		,N'ЗакрытиеРасходовОтРеализацииОС' as Имя
		,N'Закрытие расходов от реализации ОС' as Синоним
	union all select
		195 as N
		,N'ЗакрытиеРасходовОтРеализацииОСПослеПереходаПрав' as Имя
		,N'Закрытие расходов от реализации ОС (после перехода прав)' as Синоним
	union all select
		196 as N
		,N'ЗакрытиеРасходовОтРеализацииОССОтложеннымПереходомПрав' as Имя
		,N'Закрытие расходов от реализации ОС (до перехода прав)' as Синоним
	union all select
		197 as N
		,N'ЗакрытиеРасходовОтСписанияОС' as Имя
		,N'Закрытие расходов от списания ОС' as Синоним
	union all select
		198 as N
		,N'ЗакупкаВСтранахЕАЭС' as Имя
		,N'Ввоз из ЕАЭС' as Синоним
	union all select
		199 as N
		,N'ЗакупкаВСтранахЕАЭСНеотфактурованнаяПоставка' as Имя
		,N'Ввоз из ЕАЭС (неотфактурованная поставка)' as Синоним
	union all select
		200 as N
		,N'ЗакупкаВСтранахЕАЭСПоступлениеИзТоваровВПути' as Имя
		,N'Ввоз из ЕАЭС (поступление из товаров в пути)' as Синоним
	union all select
		201 as N
		,N'ЗакупкаВСтранахЕАЭСТоварыВПути' as Имя
		,N'Ввоз из ЕАЭС (товары в пути)' as Синоним
	union all select
		202 as N
		,N'ЗакупкаВСтранахЕАЭСФактуровкаПоставки' as Имя
		,N'Ввоз из ЕАЭС (фактуровка поставки)' as Синоним
	union all select
		203 as N
		,N'ЗакупкаПоИмпорту' as Имя
		,N'Импорт' as Синоним
	union all select
		204 as N
		,N'ЗакупкаПоИмпортуПоступлениеИзТоваровВПути' as Имя
		,N'Импорт (поступление из товаров в пути)' as Синоним
	union all select
		205 as N
		,N'ЗакупкаПоИмпортуТоварыВПути' as Имя
		,N'Импорт (товары в пути)' as Синоним
	union all select
		206 as N
		,N'ЗакупкаУДругойОрганизации' as Имя
		,N'Закупка у другой организации' as Синоним
	union all select
		207 as N
		,N'ЗакупкаУПоставщика' as Имя
		,N'Закупка у поставщика' as Синоним
	union all select
		208 as N
		,N'ЗакупкаУПоставщикаНеотфактурованнаяПоставка' as Имя
		,N'Закупка у поставщика (неотфактурованная поставка)' as Синоним
	union all select
		209 as N
		,N'ЗакупкаУПоставщикаПоступлениеИзТоваровВПути' as Имя
		,N'Закупка у поставщика (поступление из товаров в пути)' as Синоним
	union all select
		210 as N
		,N'ЗакупкаУПоставщикаРеглУчет' as Имя
		,N'Закупка по регл. учету' as Синоним
	union all select
		211 as N
		,N'ЗакупкаУПоставщикаТоварыВПути' as Имя
		,N'Закупка у поставщика (товары в пути)' as Синоним
	union all select
		212 as N
		,N'ЗакупкаУПоставщикаФактуровкаПоставки' as Имя
		,N'Закупка у поставщика (фактуровка поставки)' as Синоним
	union all select
		213 as N
		,N'ЗакупкаЧерезПодотчетноеЛицо' as Имя
		,N'Закупка через подотчетное лицо' as Синоним
	union all select
		214 as N
		,N'ЗаписьКнигиПокупок' as Имя
		,N'Запись книги покупок' as Синоним
	union all select
		215 as N
		,N'ЗачетАвансаВыкупнойСтоимостиВСчетВыкупнойСтоимости' as Имя
		,N'Зачет аванса выкупной стоимости в счет выкупной стоимости' as Синоним
	union all select
		216 as N
		,N'ЗачетАвансаКлиента' as Имя
		,N'Зачет аванса клиента' as Синоним
	union all select
		217 as N
		,N'ЗачетАвансаПоставщику' as Имя
		,N'Зачет аванса поставщику' as Синоним
	union all select
		218 as N
		,N'ЗачетВознагражденияАвансомКомиссионера' as Имя
		,N'Зачет вознаграждения в счет аванса комиссионера' as Синоним
	union all select
		219 as N
		,N'ЗачетВознагражденияАвансомКомитенту' as Имя
		,N'Зачет вознаграждения в счет аванса комитенту' as Синоним
	union all select
		220 as N
		,N'ЗачетВознагражденияОплатойКомиссионера' as Имя
		,N'Зачет вознаграждения оплатой комиссионера' as Синоним
	union all select
		221 as N
		,N'ЗачетВознагражденияОплатойКомитенту' as Имя
		,N'Зачет вознаграждения оплатой комитенту' as Синоним
	union all select
		222 as N
		,N'ЗачетЗемельногоНалога' as Имя
		,N'Зачет земельного налога' as Синоним
	union all select
		223 as N
		,N'ЗачетЗемельногоНалогаВСчетНалогаНаИмущество' as Имя
		,N'Зачет земельного налога в счет налога на имущество' as Синоним
	union all select
		224 as N
		,N'ЗачетЗемельногоНалогаВСчетТранспортногоНалога' as Имя
		,N'Зачет земельного налога в счет транспортного налога' as Синоним
	union all select
		225 as N
		,N'ЗачетНалогаНаИмущество' as Имя
		,N'Зачет налога на имущество' as Синоним
	union all select
		226 as N
		,N'ЗачетНалогаНаИмуществоВСчетЗемельногоНалога' as Имя
		,N'Зачет налога на имущество в счет земельного налога' as Синоним
	union all select
		227 as N
		,N'ЗачетНалогаНаИмуществоВСчетТранспортногоНалога' as Имя
		,N'Зачет налога на имущество в счет транспортного налога' as Синоним
	union all select
		228 as N
		,N'ЗачетОбеспечительногоПлатежаВСчетВыкупнойСтоимости' as Имя
		,N'Зачет обеспечительного платежа в счет выкупной стоимости' as Синоним
	union all select
		229 as N
		,N'ЗачетОплатыУслугиПоАрендеВСчетВыкупнойСтоимости' as Имя
		,N'Зачет оплаты услуги по аренде в счет выкупной стоимости' as Синоним
	union all select
		230 as N
		,N'ЗачетТранспортногоНалога' as Имя
		,N'Зачет транспортного налога' as Синоним
	union all select
		231 as N
		,N'ЗачетТранспортногоНалогаВСчетЗемельногоНалога' as Имя
		,N'Зачет транспортного налога в счет земельного налога' as Синоним
	union all select
		232 as N
		,N'ЗачетТранспортногоНалогаВСчетНалогаНаИмущество' as Имя
		,N'Зачет транспортного налога в счет налога на имущество' as Синоним
	union all select
		233 as N
		,N'ИзлишнеНачисленныеПроцентыПоАренде' as Имя
		,N'Излишне начисленные проценты по аренде' as Синоним
	union all select
		234 as N
		,N'ИзменениеДоходовБудущихПериодовОтЦелевогоФинансированияНМА' as Имя
		,N'Изменение доходов будущих периодов от целевого финансирования НМА' as Синоним
	union all select
		235 as N
		,N'ИзменениеДоходовБудущихПериодовОтЦелевогоФинансированияОС' as Имя
		,N'Изменение доходов будущих периодов от целевого финансирования ОС' as Синоним
	union all select
		236 as N
		,N'ИзменениеПараметровАмортизацииНМА' as Имя
		,N'Изменение параметров амортизации НМА' as Синоним
	union all select
		237 as N
		,N'ИзменениеПараметровАмортизацииОС' as Имя
		,N'Изменение параметров амортизации ОС' as Синоним
	union all select
		238 as N
		,N'ИзменениеПараметровНМА' as Имя
		,N'Изменение параметров НМА' as Синоним
	union all select
		239 as N
		,N'ИзменениеПараметровОС' as Имя
		,N'Изменение параметров ОС' as Синоним
	union all select
		240 as N
		,N'ИзменениеПараметровСтоимостиАрендованногоОС' as Имя
		,N'Изменение параметров стоимости арендованного ОС' as Синоним
	union all select
		241 as N
		,N'ИзменениеПараметровСтоимостиНМА' as Имя
		,N'Изменение параметров стоимости НМА' as Синоним
	union all select
		242 as N
		,N'ИзменениеПараметровСтоимостиОС' as Имя
		,N'Изменение параметров стоимости ОС' as Синоним
	union all select
		243 as N
		,N'ИзменениеСостоянияОС' as Имя
		,N'Изменение состояния ОС' as Синоним
	union all select
		244 as N
		,N'ИзменениеСпособаОтраженияИмущественныхНалогов' as Имя
		,N'Изменение способа отражения имущественных налогов' as Синоним
	union all select
		245 as N
		,N'ИзменениеУсловийДоговораАренды' as Имя
		,N'Изменение условий договора аренды' as Синоним
	union all select
		246 as N
		,N'ИнвентаризационнаяОпись' as Имя
		,N'Инвентаризационная опись' as Синоним
	union all select
		247 as N
		,N'ИнвентаризацияВложенийВОС' as Имя
		,N'Инвентаризация вложений в ОС' as Синоним
	union all select
		248 as N
		,N'ИнвентаризацияКомиссионера' as Имя
		,N'Инвентаризация комиссионера' as Синоним
	union all select
		249 as N
		,N'ИнвентаризацияНезавершенногоСтроительства' as Имя
		,N'Инвентаризация незавершенного строительства' as Синоним
	union all select
		250 as N
		,N'ИнвентаризацияНМА' as Имя
		,N'Инвентаризация НМА' as Синоним
	union all select
		251 as N
		,N'ИнвентаризацияОС' as Имя
		,N'Инвентаризация ОС' as Синоним
	union all select
		252 as N
		,N'ИнвентаризацияТМЦВЭксплуатации' as Имя
		,N'Инвентаризация ТМЦ в эксплуатации' as Синоним
	union all select
		253 as N
		,N'ИнкассацияДенежныхСредствВБанк' as Имя
		,N'Инкассация ДС в банк' as Синоним
	union all select
		254 as N
		,N'ИнкассацияДенежныхСредствИзБанка' as Имя
		,N'Инкассация ДС из банка' as Синоним
	union all select
		255 as N
		,N'ИспользованиеБронированияПодотчетнымЛицом' as Имя
		,N'Использование бронирования подотчетным лицом' as Синоним
	union all select
		256 as N
		,N'ИсправлениеОшибок' as Имя
		,N'Исправление ошибок' as Синоним
	union all select
		257 as N
		,N'ИсправлениеПрочегоНачисленияНДС' as Имя
		,N'Исправление прочего начисления НДС' as Синоним
	union all select
		258 as N
		,N'КомиссияПоЭквайрингу' as Имя
		,N'Комиссия по эквайрингу' as Синоним
	union all select
		259 as N
		,N'КонвертацияВалюты' as Имя
		,N'Конвертация валюты' as Синоним
	union all select
		260 as N
		,N'КонвертацияВалютыПодотчетнымЛицом' as Имя
		,N'Конвертация валюты подотчетным лицом' as Синоним
	union all select
		261 as N
		,N'КорректировкаАрендныхОбязательств' as Имя
		,N'Корректировка арендных обязательств' as Синоним
	union all select
		262 as N
		,N'КорректировкаВидаДеятельностиНДС' as Имя
		,N'Корректировка вида деятельности НДС' as Синоним
	union all select
		263 as N
		,N'КорректировкаДоВводаОстатков' as Имя
		,N'Корректировка до ввода остатков' as Синоним
	union all select
		264 as N
		,N'КорректировкаЗадолженности' as Имя
		,N'Корректировка задолженности' as Синоним
	union all select
		265 as N
		,N'КорректировкаНалогообложенияНДСПартийТоваров' as Имя
		,N'Корректировка налогообложения НДС партий товаров' as Синоним
	union all select
		266 as N
		,N'КорректировкаОбесцененияНМА' as Имя
		,N'Корректировка обесценения НМА' as Синоним
	union all select
		267 as N
		,N'КорректировкаОбесцененияОС' as Имя
		,N'Корректировка обесценения ОС' as Синоним
	union all select
		268 as N
		,N'КорректировкаОбособленногоУчета' as Имя
		,N'Корректировка обособленного учета' as Синоним
	union all select
		269 as N
		,N'КорректировкаОтчетаПереработчика' as Имя
		,N'Корректировка отчета переработчика' as Синоним
	union all select
		270 as N
		,N'КорректировкаПоСогласованиюСторон' as Имя
		,N'Корректировка по согласованию сторон' as Синоним
	union all select
		271 as N
		,N'КорректировкаПриобретенияПрошлогоПериода' as Имя
		,N'Корректировка приобретения прошлого периода' as Синоним
	union all select
		272 as N
		,N'КорректировкаПриобретенияСоСписаниемНаРасходы' as Имя
		,N'Корректировка приобретения со списанием на расходы' as Синоним
	union all select
		273 as N
		,N'КорректировкаПриобретенияСОтражениемНаПрочихДоходах' as Имя
		,N'Корректировка приобретения с отражением на прочих доходах' as Синоним
	union all select
		274 as N
		,N'КорректировкаПриобретенияУвеличениеЗадолженностиСводно' as Имя
		,N'Увеличение задолженности (сводно)' as Синоним
	union all select
		275 as N
		,N'КорректировкаПриобретенияУменьшениеЗадолженностиСводно' as Имя
		,N'Уменьшение задолженности (сводно)' as Синоним
	union all select
		276 as N
		,N'КорректировкаРасходовОтВыбытияОС' as Имя
		,N'Корректировка расходов от выбытия ОС' as Синоним
	union all select
		277 as N
		,N'КорректировкаРеализацииСоСписаниемНаРасходы' as Имя
		,N'Корректировка реализации со списанием на расходы' as Синоним
	union all select
		278 as N
		,N'КорректировкаРеализацииСОтражениемНаПрочихДоходах' as Имя
		,N'Корректировка реализации с отражением на прочих доходах' as Синоним
	union all select
		279 as N
		,N'КорректировкаРеализацииУвеличениеЗадолженностиСводно' as Имя
		,N'Увеличение задолженности (сводно)' as Синоним
	union all select
		280 as N
		,N'КорректировкаРеализацииУменьшениеЗадолженностиСводно' as Имя
		,N'Уменьшение задолженности (сводно)' as Синоним
	union all select
		281 as N
		,N'КорректировкаСтоимостиИАмортизацииНМА' as Имя
		,N'Корректировка стоимости и амортизации НМА' as Синоним
	union all select
		282 as N
		,N'КорректировкаСтоимостиИАмортизацииОС' as Имя
		,N'Корректировка стоимости и амортизации ОС' as Синоним
	union all select
		283 as N
		,N'КорректировкаСтоимостиТМЦОприходованныхПриВыбытииОС' as Имя
		,N'Корректировка стоимости ТМЦ оприходованных при выбытии ОС' as Синоним
	union all select
		284 as N
		,N'КурсовыеРазницыАрендаПрибыль' as Имя
		,N'Курсовые разницы по аренде (прибыль)' as Синоним
	union all select
		285 as N
		,N'КурсовыеРазницыАрендаУбыток' as Имя
		,N'Курсовые разницы по аренде (убыток)' as Синоним
	union all select
		286 as N
		,N'КурсовыеРазницыДепозитыПрибыль' as Имя
		,N'Курсовые разницы по депозитам (прибыль)' as Синоним
	union all select
		287 as N
		,N'КурсовыеРазницыДепозитыУбыток' as Имя
		,N'Курсовые разницы по депозитам (убыток)' as Синоним
	union all select
		288 as N
		,N'КурсовыеРазницыДСПрибыль' as Имя
		,N'Курсовые разницы по денежным средствам (прибыль)' as Синоним
	union all select
		289 as N
		,N'КурсовыеРазницыДСУбыток' as Имя
		,N'Курсовые разницы по денежным средствам (убыток)' as Синоним
	union all select
		290 as N
		,N'КурсовыеРазницыЗаймыВыданныеПрибыль' as Имя
		,N'Курсовые разницы по займам выданным (прибыль)' as Синоним
	union all select
		291 as N
		,N'КурсовыеРазницыЗаймыВыданныеУбыток' as Имя
		,N'Курсовые разницы по займам выданным (убыток)' as Синоним
	union all select
		292 as N
		,N'КурсовыеРазницыКлиентыПрибыль' as Имя
		,N'Курсовые разницы по расчетам с клиентами (прибыль)' as Синоним
	union all select
		293 as N
		,N'КурсовыеРазницыКлиентыУбыток' as Имя
		,N'Курсовые разницы по расчетам с клиентами (убыток)' as Синоним
	union all select
		294 as N
		,N'КурсовыеРазницыКредитыИЗаймыПрибыль' as Имя
		,N'Курсовые разницы по кредитам и займам (прибыль)' as Синоним
	union all select
		295 as N
		,N'КурсовыеРазницыКредитыИЗаймыУбыток' as Имя
		,N'Курсовые разницы по кредитам и займам (убыток)' as Синоним
	union all select
		296 as N
		,N'КурсовыеРазницыПоДисконтированиюПрибыль' as Имя
		,N'Курсовые разницы по дисконтированию (прибыль)' as Синоним
	union all select
		297 as N
		,N'КурсовыеРазницыПоДисконтированиюУбыток' as Имя
		,N'Курсовые разницы по дисконтированию (убыток)' as Синоним
	union all select
		298 as N
		,N'КурсовыеРазницыПоставщикиПрибыль' as Имя
		,N'Курсовые разницы по расчетам с поставщиками (прибыль)' as Синоним
	union all select
		299 as N
		,N'КурсовыеРазницыПоставщикиУбыток' as Имя
		,N'Курсовые разницы по расчетам с поставщиками (убыток)' as Синоним
	union all select
		300 as N
		,N'КурсовыеРазницыРезервыПоДолгамПрибыль' as Имя
		,N'Курсовые разницы резервы по сомнительным долгам (прибыль)' as Синоним
	union all select
		301 as N
		,N'КурсовыеРазницыРезервыПоДолгамУбыток' as Имя
		,N'Курсовые разницы резервы по сомнительным долгам (убыток)' as Синоним
	union all select
		302 as N
		,N'МаркировкаТоваровГИСМ' as Имя
		,N'Маркировка товаров ГИСМ' as Синоним
	union all select
		303 as N
		,N'Модернизация' as Имя
		,N'Модернизация' as Синоним
	union all select
		304 as N
		,N'МодернизацияОС' as Имя
		,N'Модернизация ОС' as Синоним
	union all select
		305 as N
		,N'НаработкаОбъектовЭксплуатации' as Имя
		,N'Наработка объектов эксплуатации' as Синоним
	union all select
		306 as N
		,N'НаработкаТМЦВЭксплуатации' as Имя
		,N'Наработка ТМЦ в эксплуатации' as Синоним
	union all select
		307 as N
		,N'НачислениеВознагражденияЗаСчетРезервов' as Имя
		,N'Начисление вознаграждения за счет резервов' as Синоним
	union all select
		308 as N
		,N'НачислениеДебиторскойЗадолженности' as Имя
		,N'Начисление дебиторской задолженности' as Синоним
	union all select
		309 as N
		,N'НачислениеДивидендов' as Имя
		,N'Начисление дивидендов' as Синоним
	union all select
		310 as N
		,N'НачислениеЗаработнойПлаты' as Имя
		,N'Начисление зарплаты' as Синоним
	union all select
		311 as N
		,N'НачислениеИмущественныхНалогов' as Имя
		,N'Начисление имущественных налогов' as Синоним
	union all select
		312 as N
		,N'НачислениеКредиторскойЗадолженности' as Имя
		,N'Начисление кредиторской задолженности' as Синоним
	union all select
		313 as N
		,N'НачислениеНалогаНаПрибыль' as Имя
		,N'Начисление налога на прибыль' as Синоним
	union all select
		314 as N
		,N'НачислениеНДСВЧастиВыкупнойСтоимости' as Имя
		,N'Начисление НДС в части выкупной стоимости' as Синоним
	union all select
		315 as N
		,N'НачислениеНДСВЧастиОбеспечительногоПлатежа' as Имя
		,N'Начисление НДС в части обеспечительного платежа' as Синоним
	union all select
		316 as N
		,N'НачислениеНДСВЧастиУслугиПоАренде' as Имя
		,N'Начисление НДС в части услуги по аренде' as Синоним
	union all select
		317 as N
		,N'НачислениеНДСНалоговымАгентом' as Имя
		,N'Начисление НДС налоговым агентом' as Синоним
	union all select
		318 as N
		,N'НачислениеНДСпоОтгрузкеТоваровВПути' as Имя
		,N'Начисление НДС по отгрузке без перехода права собственности' as Синоним
	union all select
		319 as N
		,N'НачислениеНДССПолученногоАванса' as Имя
		,N'Начисление НДС с полученного аванса' as Синоним
	union all select
		320 as N
		,N'НачислениеОценочныхОбязательствПоОтпускам' as Имя
		,N'Начисление оценочных обязательств по отпускам' as Синоним
	union all select
		321 as N
		,N'НачислениеПоДоговоруАренды' as Имя
		,N'Начисление по договору аренды' as Синоним
	union all select
		322 as N
		,N'НачислениеПроцентовПоАренде' as Имя
		,N'Начисление процентов по аренде' as Синоним
	union all select
		323 as N
		,N'НачислениеПроцентовПоДисконтированию' as Имя
		,N'Начисление процентов по дисконтированию' as Синоним
	union all select
		324 as N
		,N'НачислениеРеверсивногоНДС' as Имя
		,N'Начисление реверсивного НДС' as Синоним
	union all select
		325 as N
		,N'НачислениеРезерваПодОбесценениеЗапасов' as Имя
		,N'Начисление резерва под обесценение запасов' as Синоним
	union all select
		326 as N
		,N'НачислениеРезервовПоВознаграждениям' as Имя
		,N'Начисление резервов по вознаграждениям' as Синоним
	union all select
		327 as N
		,N'НачислениеРезервовПоСомнительнымДолгам' as Имя
		,N'Начисление резервов по сомнительным долгам' as Синоним
	union all select
		328 as N
		,N'НачислениеРезервовПоСтраховымВзносам' as Имя
		,N'Начисление резервов по страховым взносам' as Синоним
	union all select
		329 as N
		,N'НачислениеРезервовПредстоящихРасходов' as Имя
		,N'Начисление резервов предстоящих расходов' as Синоним
	union all select
		330 as N
		,N'НачислениеСписаниеРезервовПоСомнительнымДолгам' as Имя
		,N'Начисление списание резервов по сомнительным долгам' as Синоним
	union all select
		331 as N
		,N'НачислениеСписаниеРезервовПредстоящихРасходов' as Имя
		,N'Начисление списание резервов предстоящих расходов' as Синоним
	union all select
		332 as N
		,N'НачислениеТорговогоСбора' as Имя
		,N'Начисление торгового сбора' as Синоним
	union all select
		333 as N
		,N'НачисленияПоДепозитам' as Имя
		,N'Начисления по депозитам' as Синоним
	union all select
		334 as N
		,N'НачисленияПоЗаймамВыданным' as Имя
		,N'Начисления по займам выданным' as Синоним
	union all select
		335 as N
		,N'НачисленияПоКредитам' as Имя
		,N'Начисления по кредитам' as Синоним
	union all select
		336 as N
		,N'НедоначисленныеПроцентыПоАренде' as Имя
		,N'Недоначисленные проценты по аренде' as Синоним
	union all select
		337 as N
		,N'ОбеспечительныйПлатеж' as Имя
		,N'Обеспечительный платеж' as Синоним
	union all select
		338 as N
		,N'ОбеспечительныйПлатежПриУчетеЗаБалансом' as Имя
		,N'Обеспечительный платеж при учете за балансом' as Синоним
	union all select
		339 as N
		,N'ОбесценениеНМА' as Имя
		,N'Обесценение НМА' as Синоним
	union all select
		340 as N
		,N'ОбесценениеОС' as Имя
		,N'Обесценение основных средств' as Синоним
	union all select
		341 as N
		,N'ОбъединениеОС' as Имя
		,N'Объединение в новое ОС' as Синоним
	union all select
		342 as N
		,N'ОказаниеАгентскихУслуг' as Имя
		,N'Оказание агентских услуг' as Синоним
	union all select
		343 as N
		,N'ОплатаАрендодателю' as Имя
		,N'Оплата арендодателю' as Синоним
	union all select
		344 as N
		,N'ОплатаВыкупнойСтоимостиПредметовАренды' as Имя
		,N'Оплата выкупной стоимости предметов аренды' as Синоним
	union all select
		345 as N
		,N'ОплатаВыкупнойСтоимостиПредметовАрендыАванс' as Имя
		,N'Оплата выкупной стоимости предметов аренды (аванс)' as Синоним
	union all select
		346 as N
		,N'ОплатаДенежныхСредствВДругуюОрганизацию' as Имя
		,N'Оплата ДС в другую организацию' as Синоним
	union all select
		347 as N
		,N'ОплатаОбеспечительногоПлатежа' as Имя
		,N'Оплата обеспечительного платежа' as Синоним
	union all select
		348 as N
		,N'ОплатаПодарочнымСертификатом' as Имя
		,N'Оплата подарочным сертификатом' as Синоним
	union all select
		349 as N
		,N'ОплатаПоКредитам' as Имя
		,N'Оплата по кредитам и займам полученным' as Синоним
	union all select
		350 as N
		,N'ОплатаПоставщику' as Имя
		,N'Оплата поставщику' as Синоним
	union all select
		351 as N
		,N'ОплатаПоставщикуПодотчетнымЛицом' as Имя
		,N'Оплата поставщику подотчетным лицом' as Синоним
	union all select
		352 as N
		,N'ОплатаПроцентовПоКредитам' as Имя
		,N'Оплата процентов по кредитам' as Синоним
	union all select
		353 as N
		,N'ОплатаУслугПоАренде' as Имя
		,N'Оплата услуг по аренде' as Синоним
	union all select
		354 as N
		,N'ОприходованиеЗаСчетДоходов' as Имя
		,N'Оприходование (за счет доходов/пассивов)' as Синоним
	union all select
		355 as N
		,N'ОприходованиеЗаСчетРасходов' as Имя
		,N'Оприходование (за счет расходов/активов)' as Синоним
	union all select
		356 as N
		,N'ОприходованиеИзлишковТоваровВПользуКомитента' as Имя
		,N'Оприходование излишков товаров в пользу комитента' as Синоним
	union all select
		357 as N
		,N'ОприходованиеИзлишковТоваровВПользуПоклажедателя' as Имя
		,N'Оприходование излишков в пользу поклажедателя' as Синоним
	union all select
		358 as N
		,N'ОприходованиеПоВозврату' as Имя
		,N'Оприходование по возврату' as Синоним
	union all select
		359 as N
		,N'ОприходованиеПриВыбытииОС' as Имя
		,N'Оприходование (при выбытии ОС)' as Синоним
	union all select
		360 as N
		,N'ОприходованиеТМЦВЭксплуатации' as Имя
		,N'Оприходование ТМЦ в эксплуатации' as Синоним
	union all select
		361 as N
		,N'ОприходованиеТоваров' as Имя
		,N'Оприходование товаров' as Синоним
	union all select
		362 as N
		,N'ОтгрузкаБезПереходаПраваСобственности' as Имя
		,N'Отгрузка (товары в пути)' as Синоним
	union all select
		363 as N
		,N'ОтгрузкаПринятыхСПравомПродажиТоваровСХранения' as Имя
		,N'Отгрузка принятых с правом продажи товаров с хранения' as Синоним
	union all select
		364 as N
		,N'ОтклонениеВСтоимостиТоваровДоходы' as Имя
		,N'Отклонение в стоимости товаров (доходы)' as Синоним
	union all select
		365 as N
		,N'ОтклонениеВСтоимостиТоваровРасходы' as Имя
		,N'Отклонение в стоимости товаров (расходы)' as Синоним
	union all select
		366 as N
		,N'ОтклоненияВСтоимостиДенежныхДокументовДоходы' as Имя
		,N'Отклонения в стоимости денежных документов (доходы)' as Синоним
	union all select
		367 as N
		,N'ОтклоненияВСтоимостиДенежныхДокументовРасходы' as Имя
		,N'Отклонения в стоимости денежных документов (расходы)' as Синоним
	union all select
		368 as N
		,N'ОтражениеАрендныхОбязательствВДоходах' as Имя
		,N'Отражение арендных обязательств в доходах' as Синоним
	union all select
		369 as N
		,N'ОтражениеАрендныхОбязательствВРасходах' as Имя
		,N'Отражение арендных обязательств в расходах' as Синоним
	union all select
		370 as N
		,N'ОтражениеВозвратаОплатыЧерезКомиссионера' as Имя
		,N'Отражение возврата оплаты через комиссионера' as Синоним
	union all select
		371 as N
		,N'ОтражениеЗадолженностиПередКомитентом' as Имя
		,N'Отражение задолженности перед комитентом' as Синоним
	union all select
		372 as N
		,N'ОтражениеЗаработнойПлаты' as Имя
		,N'Отражение заработной платы' as Синоним
	union all select
		373 as N
		,N'ОтражениеИзлишкаПриИнвентаризацииДенежныхСредств' as Имя
		,N'Отражение излишка при инвентаризации денежных средств' as Синоним
	union all select
		374 as N
		,N'ОтражениеИзлишкаПриИнкассацииДенежныхСредств' as Имя
		,N'Отражение излишка при инкассации денежных средств' as Синоним
	union all select
		375 as N
		,N'ОтражениеИзлишковНаДоходыПриПоступленииТоваров' as Имя
		,N'Отражение излишков на доходы при поступлении товаров' as Синоним
	union all select
		376 as N
		,N'ОтражениеНалоговВзносовСЗаработнойПлаты' as Имя
		,N'Отражение налогов взносов с заработной платы' as Синоним
	union all select
		377 as N
		,N'ОтражениеНалоговВзносовСоСдельнойЗаработнойПлаты' as Имя
		,N'Отражение налогов взносов со сдельной заработной платы' as Синоним
	union all select
		378 as N
		,N'ОтражениеНДФЛ' as Имя
		,N'Отражение НДФЛ' as Синоним
	union all select
		379 as N
		,N'ОтражениеНедостачЗаСчетПоставщикаПриПоступленииТоваров' as Имя
		,N'Отражение недостач за счет поставщика при поступлении товаров' as Синоним
	union all select
		380 as N
		,N'ОтражениеНедостачЗаСчетСтороннейКомпанииПриПоступленииТоваров' as Имя
		,N'Отражение недостач за счет сторонней компании при поступлении товаров' as Синоним
	union all select
		381 as N
		,N'ОтражениеНедостачиПриИнвентаризацииДенежныхСредств' as Имя
		,N'Отражение недостачи при инвентаризации денежных средств' as Синоним
	union all select
		382 as N
		,N'ОтражениеНедостачиПриИнкассацииДенежныхСредств' as Имя
		,N'Отражение недостачи при инкассации денежных средств' as Синоним
	union all select
		383 as N
		,N'ОтражениеНедостачНаРасходыПриПоступленииТоваров' as Имя
		,N'Отражение недостач на расходы при поступлении товаров' as Синоним
	union all select
		384 as N
		,N'ОтражениеОплатыЧерезКомиссионера' as Имя
		,N'Отражение оплаты через комиссионера' as Синоним
	union all select
		385 as N
		,N'ОтражениеПлановойСтоимостиВыпуска' as Имя
		,N'Отражение плановой стоимости выпуска' as Синоним
	union all select
		386 as N
		,N'ОтражениеПрочихАктивовПассивов' as Имя
		,N'Отражение прочих активов/пассивов' as Синоним
	union all select
		387 as N
		,N'ОтражениеРасходовЗаСчетПрочихАктивовПассивов' as Имя
		,N'Отражение расходов за счет прочих активов/пассивов' as Синоним
	union all select
		388 as N
		,N'ОтражениеСдельнойЗаработнойПлаты' as Имя
		,N'Отражение сдельной заработной платы' as Синоним
	union all select
		389 as N
		,N'ОтражениеУслугПоАрендеВРасходах' as Имя
		,N'Отражение услуг по аренде в расходах' as Синоним
	union all select
		390 as N
		,N'ОтчетБанкаПоОперациямЭквайринга' as Имя
		,N'Отчет банка по операциям эквайринга' as Синоним
	union all select
		391 as N
		,N'ОтчетДавальцу' as Имя
		,N'Отчет давальцу (2.4)' as Синоним
	union all select
		392 as N
		,N'ОтчетДавальцу2_5' as Имя
		,N'Отчет давальцу' as Синоним
	union all select
		393 as N
		,N'ОтчетДавальцуКорректировкаПрошлогоПериода' as Имя
		,N'Отчет давальцу корректировка прошлого периода' as Синоним
	union all select
		394 as N
		,N'ОтчетДавальцуСписаниеНаРасходы' as Имя
		,N'Отчет давальцу (списание на расходы)' as Синоним
	union all select
		395 as N
		,N'ОтчетДавальцуСторно' as Имя
		,N'Отчет давальцу сторно' as Синоним
	union all select
		396 as N
		,N'ОтчетКомиссионера' as Имя
		,N'Отчет комиссионера' as Синоним
	union all select
		397 as N
		,N'ОтчетКомиссионераКомиссия' as Имя
		,N'Отчет комиссионера (комиссионное вознаграждение)' as Синоним
	union all select
		398 as N
		,N'ОтчетКомиссионераОСписании' as Имя
		,N'Отчет комиссионера о списании' as Синоним
	union all select
		399 as N
		,N'ОтчетКомитенту' as Имя
		,N'Отчет комитенту' as Синоним
	union all select
		400 as N
		,N'ОтчетКомитентуКомиссия' as Имя
		,N'Отчет комитенту (комиссионное вознаграждение)' as Синоним
	union all select
		401 as N
		,N'ОтчетКомитентуОСписании' as Имя
		,N'Отчет комитенту о списании' as Синоним
	union all select
		402 as N
		,N'ОтчетПоКомиссииМеждуОрганизациями' as Имя
		,N'Отчет по комиссии между организациями' as Синоним
	union all select
		403 as N
		,N'ОтчетПоКомиссииМеждуОрганизациямиКомиссия' as Имя
		,N'Отчет по комиссии между организациями (комиссионное вознаграждение)' as Синоним
	union all select
		404 as N
		,N'ОтчетПоКомиссииМеждуОрганизациямиОСписании' as Имя
		,N'Отчет по комиссии между организациями о списании' as Синоним
	union all select
		405 as N
		,N'ОтчетПринципалуОЗакупках' as Имя
		,N'Отчет принципалу о закупках' as Синоним
	union all select
		406 as N
		,N'ОтчетПринципалуОЗакупкахКомиссия' as Имя
		,N'Отчет принципалу о закупках (комиссионное вознаграждение)' as Синоним
	union all select
		407 as N
		,N'ОформлениеГТДБрокером' as Имя
		,N'Оформление ГТД через брокера' as Синоним
	union all select
		408 as N
		,N'ОформлениеГТДСамостоятельно' as Имя
		,N'Самостоятельное оформление ГТД' as Синоним
	union all select
		409 as N
		,N'ОформлениеТаможеннойДекларацииЭкспорт' as Имя
		,N'Оформление таможенной декларации на экспорт' as Синоним
	union all select
		410 as N
		,N'ПараметрыНачисленияЗемельногоНалога' as Имя
		,N'Параметры начисления земельного налога' as Синоним
	union all select
		411 as N
		,N'ПараметрыНачисленияНалогаНаИмущество' as Имя
		,N'Параметры начисления налога на имущество' as Синоним
	union all select
		412 as N
		,N'ПараметрыНачисленияТранспортногоНалога' as Имя
		,N'Параметры начисления транспортного налога' as Синоним
	union all select
		413 as N
		,N'ПереводОсновныхСредствИнвестиционногоИмущества' as Имя
		,N'Перевод основных средств и инвестиционного имущества' as Синоним
	union all select
		414 as N
		,N'ПередачаВПроизводство' as Имя
		,N'Передача в производство' as Синоним
	union all select
		415 as N
		,N'ПередачаВСоставНМА' as Имя
		,N'Передача в состав НМА и НИОКР' as Синоним
	union all select
		416 as N
		,N'ПередачаВСоставОС' as Имя
		,N'Передача в состав основных средств' as Синоним
	union all select
		417 as N
		,N'ПередачаВЭксплуатацию' as Имя
		,N'Передача в эксплуатацию' as Синоним
	union all select
		418 as N
		,N'ПередачаВЭксплуатациюБУНУ' as Имя
		,N'Передача в эксплуатацию (БУ и НУ)' as Синоним
	union all select
		419 as N
		,N'ПередачаДавальцу' as Имя
		,N'Передача давальцу (2.4)' as Синоним
	union all select
		420 as N
		,N'ПередачаДавальцу2_5' as Имя
		,N'Передача давальцу' as Синоним
	union all select
		421 as N
		,N'ПередачаМатериаловВКладовую' as Имя
		,N'Передача материалов в кладовую' as Синоним
	union all select
		422 as N
		,N'ПередачаМатериаловВПроизводство' as Имя
		,N'Передача материалов в производство' as Синоним
	union all select
		423 as N
		,N'ПередачаНаКомиссию' as Имя
		,N'Передача на комиссию' as Синоним
	union all select
		424 as N
		,N'ПередачаНаКомиссиюВДругуюОрганизацию' as Имя
		,N'Передача на комиссию в другую организацию' as Синоним
	union all select
		425 as N
		,N'ПередачаНаПрочиеЦели' as Имя
		,N'Передача на прочие цели' as Синоним
	union all select
		426 as N
		,N'ПередачаНаХранениеСПравомПродажи' as Имя
		,N'Передача на хранение с правом продажи' as Синоним
	union all select
		427 as N
		,N'ПередачаОСВАренду' as Имя
		,N'Передача ОС в аренду' as Синоним
	union all select
		428 as N
		,N'ПередачаПереработчику' as Имя
		,N'Передача переработчику (2.4)' as Синоним
	union all select
		429 as N
		,N'ПередачаПереработчику2_5' as Имя
		,N'Передача переработчику' as Синоним
	union all select
		430 as N
		,N'ПередачаПлатежаИзФилиала' as Имя
		,N'Передача платежа из филиала' as Синоним
	union all select
		431 as N
		,N'ПередачаПродукцииИзКладовой' as Имя
		,N'Передача продукции из кладовой' as Синоним
	union all select
		432 as N
		,N'ПередачаПродукцииИзПроизводства' as Имя
		,N'Передача продукции из производства' as Синоним
	union all select
		433 as N
		,N'ПередачаПродукцииИзПроизводстваФиксированнаяСтоимость' as Имя
		,N'Передача продукции из производства (фикс. стоимость)' as Синоним
	union all select
		434 as N
		,N'ПередачаПрочихРасходовМеждуФилиалами' as Имя
		,N'Передача прочих расходов между филиалами' as Синоним
	union all select
		435 as N
		,N'ПеремаркировкаТоваровГИСМ' as Имя
		,N'Перемаркировка товаров ГИСМ' as Синоним
	union all select
		436 as N
		,N'ПеремещениеАмортизацииНМАвДругуюОрганизацию' as Имя
		,N'Перемещение амортизации НМА в другую организацию' as Синоним
	union all select
		437 as N
		,N'ПеремещениеАмортизацииНМАизДругойОрганизации' as Имя
		,N'Перемещение амортизации НМА из другой организации' as Синоним
	union all select
		438 as N
		,N'ПеремещениеАмортизацииОСвДругуюОрганизацию' as Имя
		,N'Перемещение амортизации ОС в другую организацию' as Синоним
	union all select
		439 as N
		,N'ПеремещениеАмортизацииОСизДругойОрганизации' as Имя
		,N'Перемещение амортизации ОС из другой организации' as Синоним
	union all select
		440 as N
		,N'ПеремещениеВЭксплуатации' as Имя
		,N'Перемещение в эксплуатации' as Синоним
	union all select
		441 as N
		,N'ПеремещениеДенежныхДокументов' as Имя
		,N'Перемещение денежных документов' as Синоним
	union all select
		442 as N
		,N'ПеремещениеМатериаловВПроизводстве' as Имя
		,N'Перемещение материалов в производстве' as Синоним
	union all select
		443 as N
		,N'ПеремещениеНМА' as Имя
		,N'Перемещение НМА' as Синоним
	union all select
		444 as N
		,N'ПеремещениеНМАвПодразделениеВыделенноеНаБаланс' as Имя
		,N'Перемещение НМА в подразделение, выделенное на баланс' as Синоним
	union all select
		445 as N
		,N'ПеремещениеОС' as Имя
		,N'Перемещение ОС' as Синоним
	union all select
		446 as N
		,N'ПеремещениеОСвПодразделениеВыделенноеНаБаланс' as Имя
		,N'Перемещение ОС в подразделение, выделенное на баланс' as Синоним
	union all select
		447 as N
		,N'ПеремещениеОСпоИнвентаризации' as Имя
		,N'Перемещение ОС по инвентаризации' as Синоним
	union all select
		448 as N
		,N'ПеремещениеПолуфабрикатов' as Имя
		,N'Перемещение полуфабрикатов' as Синоним
	union all select
		449 as N
		,N'ПеремещениеПолуфабрикатовМеждуФилиалами' as Имя
		,N'Перемещение полуфабрикатов между филиалами' as Синоним
	union all select
		450 as N
		,N'ПеремещениеСтоимостиНМАвДругуюОрганизацию' as Имя
		,N'Перемещение стоимости НМА в другую организацию' as Синоним
	union all select
		451 as N
		,N'ПеремещениеСтоимостиНМАизДругойОрганизации' as Имя
		,N'Перемещение стоимости НМА из другой организации' as Синоним
	union all select
		452 as N
		,N'ПеремещениеСтоимостиОСвДругуюОрганизацию' as Имя
		,N'Перемещение стоимости ОС в другую организацию' as Синоним
	union all select
		453 as N
		,N'ПеремещениеСтоимостиОСизДругойОрганизации' as Имя
		,N'Перемещение стоимости ОС из другой организации' as Синоним
	union all select
		454 as N
		,N'ПеремещениеТоваров' as Имя
		,N'Перемещение товаров' as Синоним
	union all select
		455 as N
		,N'ПеремещениеТоваровМеждуФилиалами' as Имя
		,N'Перемещение товаров между филиалами' as Синоним
	union all select
		456 as N
		,N'ПеремещениеУзлов' as Имя
		,N'Перемещение узлов' as Синоним
	union all select
		457 as N
		,N'ПереносАванса' as Имя
		,N'Перенос аванса' as Синоним
	union all select
		458 as N
		,N'ПереносДолга' as Имя
		,N'Перенос долга' as Синоним
	union all select
		459 as N
		,N'ПереносЗадолженностиМеждуФилиалами' as Имя
		,N'Перенос задолженности между филиалами' as Синоним
	union all select
		460 as N
		,N'ПереносПлатежаМеждуФилиалами' as Имя
		,N'Перенос платежа между филиалами' as Синоним
	union all select
		461 as N
		,N'ПереносПретензииНаАвансы' as Имя
		,N'Перенос претензии на авансы' as Синоним
	union all select
		462 as N
		,N'ПереносПретензииНаРасчеты' as Имя
		,N'Перенос претензии на расчеты' as Синоним
	union all select
		463 as N
		,N'ПереоценкаДенежныхСредств' as Имя
		,N'Переоценка денежных средств' as Синоним
	union all select
		464 as N
		,N'ПереоценкаНМА' as Имя
		,N'Переоценка НМА' as Синоним
	union all select
		465 as N
		,N'ПереоценкаОС' as Имя
		,N'Переоценка ОС' as Синоним
	union all select
		466 as N
		,N'ПереоценкаРасчетовПоАренде' as Имя
		,N'Переоценка расчетов по аренде' as Синоним
	union all select
		467 as N
		,N'ПереоценкаРасчетовСКлиентами' as Имя
		,N'Переоценка расчетов с клиентами' as Синоним
	union all select
		468 as N
		,N'ПереоценкаРасчетовСПоставщиками' as Имя
		,N'Переоценка расчетов с поставщиками' as Синоним
	union all select
		469 as N
		,N'ПереоценкаРезервовПоСомнительнымДолгам' as Имя
		,N'Переоценка резервов по сомнительным долгам' as Синоним
	union all select
		470 as N
		,N'ПереоценкаСуммДисконтирования' as Имя
		,N'Переоценка сумм дисконтирования' as Синоним
	union all select
		471 as N
		,N'ПереоценкаФинансовыхИнструментов' as Имя
		,N'Переоценка финансовых инструментов' as Синоним
	union all select
		472 as N
		,N'ПерерасчетЗемельногоНалога' as Имя
		,N'Перерасчет земельного налога' as Синоним
	union all select
		473 as N
		,N'ПерерасчетИмущественныхНалогов' as Имя
		,N'Перерасчет имущественных налогов' as Синоним
	union all select
		474 as N
		,N'ПерерасчетНалогаНаИмущество' as Имя
		,N'Перерасчет налога на имущество' as Синоним
	union all select
		475 as N
		,N'ПерерасчетТранспортногоНалога' as Имя
		,N'Перерасчет транспортного налога' as Синоним
	union all select
		476 as N
		,N'ПересортицаПартийТоваров' as Имя
		,N'Пересортица партий товаров' as Синоним
	union all select
		477 as N
		,N'ПересортицаТоваров' as Имя
		,N'Пересортица товаров' as Синоним
	union all select
		478 as N
		,N'ПересортицаТоваровСПереоценкой' as Имя
		,N'Пересортица товаров (переоценка)' as Синоним
	union all select
		479 as N
		,N'ПересортицаТоваровУПереработчика' as Имя
		,N'Пересортица товаров у переработчика' as Синоним
	union all select
		480 as N
		,N'ПересортицаТоваровУХранителя' as Имя
		,N'Пересортица товаров у хранителя' as Синоним
	union all select
		481 as N
		,N'ПеречислениеВБюджет' as Имя
		,N'Перечисление налогов и взносов' as Синоним
	union all select
		482 as N
		,N'ПеречислениеДенежныхСредствНаДругойСчет' as Имя
		,N'Перечисление ДС на другой счет' as Синоним
	union all select
		483 as N
		,N'ПеречислениеНаДепозиты' as Имя
		,N'Перечисление на депозиты' as Синоним
	union all select
		484 as N
		,N'ПеречислениеТаможне' as Имя
		,N'Таможенный платеж' as Синоним
	union all select
		485 as N
		,N'ПланированиеПоЗаказуКлиента' as Имя
		,N'Планирование оплаты от клиента' as Синоним
	union all select
		486 as N
		,N'ПланированиеПоЗаказуПоставщику' as Имя
		,N'Планирование оплаты поставщику' as Синоним
	union all select
		487 as N
		,N'ПланированиеПоЗаявке' as Имя
		,N'Планирование по заявке' as Синоним
	union all select
		488 as N
		,N'ПланированиеПоСчету' as Имя
		,N'Планирование по счету' as Синоним
	union all select
		489 as N
		,N'ПогашениеЗадолженностиКлиента' as Имя
		,N'Погашение задолженности клиента' as Синоним
	union all select
		490 as N
		,N'ПогашениеЗадолженностиПоставщику' as Имя
		,N'Погашение задолженности поставщику' as Синоним
	union all select
		491 as N
		,N'ПогашениеЗаймаСотрудником' as Имя
		,N'Погашение займа сотрудником' as Синоним
	union all select
		492 as N
		,N'ПогашениеСтоимостиТМЦВЭксплуатации' as Имя
		,N'Погашение стоимости ТМЦ в эксплуатации' as Синоним
	union all select
		493 as N
		,N'ПодготовкаКПередачеНМА' as Имя
		,N'Подготовка к передаче НМА' as Синоним
	union all select
		494 as N
		,N'ПодготовкаКПередачеОС' as Имя
		,N'Подготовка к передаче ОС' as Синоним
	union all select
		495 as N
		,N'ПокупкаПолученнойВозвратнойТары' as Имя
		,N'Покупка полученной возвратной тары' as Синоним
	union all select
		496 as N
		,N'ПорчаТоваров' as Имя
		,N'Порча товаров' as Синоним
	union all select
		497 as N
		,N'ПорчаТоваровСПереоценкой' as Имя
		,N'Порча товаров с переоценкой' as Синоним
	union all select
		498 as N
		,N'ПорчаТоваровУПереработчика' as Имя
		,N'Порча товаров у переработчика' as Синоним
	union all select
		499 as N
		,N'ПорчаТоваровУХранителя' as Имя
		,N'Порча товаров у хранителя' as Синоним
	union all select
		500 as N
		,N'ПоставкаПодПринципала' as Имя
		,N'Поставка под принципала' as Синоним
	union all select
		501 as N
		,N'ПоступлениеАрендованныхОС' as Имя
		,N'Поступление арендованных ОС (забалансовый учет)' as Синоним
	union all select
		502 as N
		,N'ПоступлениеДенежныхДокументовОтПодотчетника' as Имя
		,N'Поступление денежных документов от подотчетного лица' as Синоним
	union all select
		503 as N
		,N'ПоступлениеДенежныхДокументовОтПоставщика' as Имя
		,N'Поступление денежных документов от поставщика' as Синоним
	union all select
		504 as N
		,N'ПоступлениеДенежныхСредствИзБанка' as Имя
		,N'Поступление ДС из банка' as Синоним
	union all select
		505 as N
		,N'ПоступлениеДенежныхСредствИзДругойКассы' as Имя
		,N'Поступление ДС из другой кассы' as Синоним
	union all select
		506 as N
		,N'ПоступлениеДенежныхСредствИзДругойОрганизации' as Имя
		,N'Поступление ДС от другой организации' as Синоним
	union all select
		507 as N
		,N'ПоступлениеДенежныхСредствИзКассыККМ' as Имя
		,N'Поступление ДС из кассы ККМ' as Синоним
	union all select
		508 as N
		,N'ПоступлениеДенежныхСредствИзКассыНаРасчетныйСчет' as Имя
		,N'Инкассация ДС из кассы на расчетный счет' as Синоним
	union all select
		509 as N
		,N'ПоступлениеДенежныхСредствОтКонвертацииВалюты' as Имя
		,N'Поступление ДС от конвертации валюты' as Синоним
	union all select
		510 as N
		,N'ПоступлениеДенежныхСредствПоДепозитам' as Имя
		,N'Поступление ДС по депозитам' as Синоним
	union all select
		511 as N
		,N'ПоступлениеДенежныхСредствПоЗаймамВыданным' as Имя
		,N'Погашение займа контрагентом' as Синоним
	union all select
		512 as N
		,N'ПоступлениеДенежныхСредствПоКредитам' as Имя
		,N'Поступление по кредитам и займам полученным' as Синоним
	union all select
		513 as N
		,N'ПоступлениеДенежныхСредствСДругогоСчета' as Имя
		,N'Поступление ДС с другого счета' as Синоним
	union all select
		514 as N
		,N'ПоступлениеЗатрат' as Имя
		,N'Поступление затрат' as Синоним
	union all select
		515 as N
		,N'ПоступлениеИзПроизводства' as Имя
		,N'Поступление из производства' as Синоним
	union all select
		516 as N
		,N'ПоступлениеНДСВЧастиВыкупнойСтоимости' as Имя
		,N'Поступление НДС в части выкупной стоимости' as Синоним
	union all select
		517 as N
		,N'ПоступлениеНДСВЧастиОбеспечительногоПлатежа' as Имя
		,N'Поступление НДС в части обеспечительного платежа' as Синоним
	union all select
		518 as N
		,N'ПоступлениеНДСВЧастиУслугиПоАренде' as Имя
		,N'Поступление НДС в части услуги по аренде' as Синоним
	union all select
		519 as N
		,N'ПоступлениеНМА' as Имя
		,N'Поступление НМА и НИОКР' as Синоним
	union all select
		520 as N
		,N'ПоступлениеОбъектовСтроительства' as Имя
		,N'Поступление объектов строительства' as Синоним
	union all select
		521 as N
		,N'ПоступлениеОплатыОтКлиента' as Имя
		,N'Поступление оплаты от клиента' as Синоним
	union all select
		522 as N
		,N'ПоступлениеОплатыОтКлиентаПоПлатежнойКарте' as Имя
		,N'Поступление ДС по эквайринговым операциям' as Синоним
	union all select
		523 as N
		,N'ПоступлениеОплатыПоПлатежнойКарте' as Имя
		,N'Поступление оплаты по эквайрингу' as Синоним
	union all select
		524 as N
		,N'ПоступлениеОС' as Имя
		,N'Поступление основных средств' as Синоним
	union all select
		525 as N
		,N'ПоступлениеОтДавальца' as Имя
		,N'Поступление от давальца (2.4)' as Синоним
	union all select
		526 as N
		,N'ПоступлениеОтДавальца2_5' as Имя
		,N'Поступление от давальца' as Синоним
	union all select
		527 as N
		,N'ПоступлениеОтПереработчика' as Имя
		,N'Поступление от переработчика (2.4)' as Синоним
	union all select
		528 as N
		,N'ПоступлениеОтПереработчика2_5' as Имя
		,N'Поступление от переработчика' as Синоним
	union all select
		529 as N
		,N'ПоступлениеОтПереработчикаФиксированнаяСтоимость' as Имя
		,N'Поступление от переработчика фиксированная стоимость' as Синоним
	union all select
		530 as N
		,N'ПоступлениеПроцентовПоЗаймамВыданным' as Имя
		,N'Поступление процентов по займам выданным' as Синоним
	union all select
		531 as N
		,N'ПоступлениеПрочихАктивов' as Имя
		,N'Поступление прочих активов' as Синоним
	union all select
		532 as N
		,N'ПоступлениеПрочихУслуг' as Имя
		,N'Поступление прочих услуг' as Синоним
	union all select
		533 as N
		,N'ПоступлениеУслуг' as Имя
		,N'Поступление услуг' as Синоним
	union all select
		534 as N
		,N'ПоступлениеУслугДляПроизводства' as Имя
		,N'Поступление услуг для производства' as Синоним
	union all select
		535 as N
		,N'ПоступлениеУслугПоАренде' as Имя
		,N'Поступление услуг по аренде' as Синоним
	union all select
		536 as N
		,N'ПоступлениеУслугРеглУчет' as Имя
		,N'Поступление услуг (закупка по регл.)' as Синоним
	union all select
		537 as N
		,N'ПрекращениеДоговораАренды' as Имя
		,N'Прекращение договора аренды' as Синоним
	union all select
		538 as N
		,N'ПриемкаПодПринципала' as Имя
		,N'Приемка под принципала' as Синоним
	union all select
		539 as N
		,N'ПриемНаКомиссию' as Имя
		,N'Прием на комиссию' as Синоним
	union all select
		540 as N
		,N'ПриемНаХранениеСПравомПродажи' as Имя
		,N'Прием на хранение с правом продажи' as Синоним
	union all select
		541 as N
		,N'ПриемОплатыОтКомиссионера' as Имя
		,N'Прием оплаты от комиссионера' as Синоним
	union all select
		542 as N
		,N'ПриемПередачаРаботМеждуПодразделениями' as Имя
		,N'Прием-передача работ между подразделениями' as Синоним
	union all select
		543 as N
		,N'ПриемПередачаРаботМеждуФилиалами' as Имя
		,N'Прием-передача работ между филиалами' as Синоним
	union all select
		544 as N
		,N'ПриемПлатежаВФилиале' as Имя
		,N'Прием платежа в филиале' as Синоним
	union all select
		545 as N
		,N'ПризнаниеВНУАрендныхПлатежей' as Имя
		,N'Признание в НУ арендных платежей' as Синоним
	union all select
		546 as N
		,N'ПризнаниеРасходовПоИсследованиям' as Имя
		,N'Признание расходов по исследованиям' as Синоним
	union all select
		547 as N
		,N'ПринятиеКУчетуНМА' as Имя
		,N'Принятие к учету НМА' as Синоним
	union all select
		548 as N
		,N'ПринятиеКУчетуНМАпоИнвентаризации' as Имя
		,N'Принятие к учету НМА по инвентаризации' as Синоним
	union all select
		549 as N
		,N'ПринятиеКУчетуОС' as Имя
		,N'Принятие к учету ОС' as Синоним
	union all select
		550 as N
		,N'ПринятиеКУчетуОСпоИнвентаризации' as Имя
		,N'Принятие к учету ОС по инвентаризации' as Синоним
	union all select
		551 as N
		,N'ПринятиеКУчетуПредметовАренды' as Имя
		,N'Принятие к учету предметов аренды' as Синоним
	union all select
		552 as N
		,N'ПринятиеКУчетуСамортизированногоОС' as Имя
		,N'Принятие к учету самортизированного ОС' as Синоним
	union all select
		553 as N
		,N'ПринятиеКУчетуУзловКомпонентовАмортизации' as Имя
		,N'Принятие к учету узлов и компонентов амортизации' as Синоним
	union all select
		554 as N
		,N'ПринятиеНДСкВычету' as Имя
		,N'Принятие НДС к вычету' as Синоним
	union all select
		555 as N
		,N'ПрисоединениеОС' as Имя
		,N'Присоединение к существующему ОС' as Синоним
	union all select
		556 as N
		,N'ПрисоединениеРезервовПоСомнительнымДолгамКДоходам' as Имя
		,N'Присоединение резервов по сомнительным долгам к доходам' as Синоним
	union all select
		557 as N
		,N'ПрисоединениеРезервовПоСомнительнымДолгамКРасходам' as Имя
		,N'Присоединение резервов по сомнительным долгам к расходам' as Синоним
	union all select
		558 as N
		,N'ПроизводствоИзДавальческогоСырья' as Имя
		,N'Производство из давальческого сырья (2.4)' as Синоним
	union all select
		559 as N
		,N'ПроизводствоИзДавальческогоСырья2_5' as Имя
		,N'Производство из давальческого сырья' as Синоним
	union all select
		560 as N
		,N'ПроизводствоУПереработчика' as Имя
		,N'Производство у переработчика (2.4)' as Синоним
	union all select
		561 as N
		,N'ПроизводствоУПереработчика2_5' as Имя
		,N'Производство у переработчика' as Синоним
	union all select
		562 as N
		,N'ПроизводствоУПереработчикаВСтранахЕАЭС2_5' as Имя
		,N'Производство у переработчика (в странах ЕАЭС)' as Синоним
	union all select
		563 as N
		,N'ПрочаяВыдачаДенежныхСредств' as Имя
		,N'Прочий расход ДС' as Синоним
	union all select
		564 as N
		,N'ПрочееНачислениеНДС' as Имя
		,N'Прочее начисление НДС' as Синоним
	union all select
		565 as N
		,N'ПрочееПоступлениеДенежныхСредств' as Имя
		,N'Прочее поступление ДС' as Синоним
	union all select
		566 as N
		,N'ПрочиеДоходы' as Имя
		,N'Прочие доходы' as Синоним
	union all select
		567 as N
		,N'ПрочиеДоходыАктивыПассивы' as Имя
		,N'Прочие доходы за счет прочих активов/пассивов' as Синоним
	union all select
		568 as N
		,N'ПрочиеРасходы' as Имя
		,N'Прочие расходы' as Синоним
	union all select
		569 as N
		,N'ПрочиеРасходыАктивыПассивы' as Имя
		,N'Прочие расходы за счет прочих активов/пассивов' as Синоним
	union all select
		570 as N
		,N'ПрочиеРасходыПодотчетногоЛица' as Имя
		,N'Прочие расходы подотчетного лица' as Синоним
	union all select
		571 as N
		,N'РазборкаТоваров' as Имя
		,N'Разборка на комплектующие' as Синоним
	union all select
		572 as N
		,N'РазукомплектацияОСПолная' as Имя
		,N'Разукомплектация ОС' as Синоним
	union all select
		573 as N
		,N'РазукомплектацияОСЧастичная' as Имя
		,N'Частичная разукомплектация ОС' as Синоним
	union all select
		574 as N
		,N'РаспределениеДоходовПоНаправлениямДеятельности' as Имя
		,N'Распределение доходов по направлениям деятельности' as Синоним
	union all select
		575 as N
		,N'РаспределениеНДС' as Имя
		,N'Распределение НДС' as Синоним
	union all select
		576 as N
		,N'РаспределениеНормируемыхРасходовПоНУ' as Имя
		,N'Распределение нормируемых расходов по НУ' as Синоним
	union all select
		577 as N
		,N'РаспределениеРасходовНаОВЗ' as Имя
		,N'Распределение расходов на объекты возникновения затрат' as Синоним
	union all select
		578 as N
		,N'РаспределениеРасходовНаПартииПроизводства' as Имя
		,N'Распределение расходов на партии производства' as Синоним
	union all select
		579 as N
		,N'РаспределениеРасходовНаСебестоимость' as Имя
		,N'Распределение расходов на себестоимость' as Синоним
	union all select
		580 as N
		,N'РаспределениеРасходовНаСебестоимостьПродаж' as Имя
		,N'Распределение расходов на себестоимость продаж' as Синоним
	union all select
		581 as N
		,N'РаспределениеРасходовНаСебестоимостьПроизводства' as Имя
		,N'Распределение расходов на себестоимость производства' as Синоним
	union all select
		582 as N
		,N'РаспределениеРасходовПоНаправлениямДеятельности' as Имя
		,N'Распределение расходов по направлениям деятельности' as Синоним
	union all select
		583 as N
		,N'РаспределениеРБП' as Имя
		,N'Распределение расходов будущих периодов' as Синоним
	union all select
		584 as N
		,N'РасходыНаТаможенныеСборыШтрафы' as Имя
		,N'Расходы на таможенные сборы (штрафы)' as Синоним
	union all select
		585 as N
		,N'РасходыОтПереоценкиТоваров' as Имя
		,N'Расходы от переоценки товаров' as Синоним
	union all select
		586 as N
		,N'РасходыОтСписанияАктиваСОтложеннымПереходомПрав' as Имя
		,N'Расходы от списания актива с отложенным переходом прав' as Синоним
	union all select
		587 as N
		,N'РасчетРезервовПодОбесценениеЗапасов' as Имя
		,N'Расчет резервов под обесценение запасов' as Синоним
	union all select
		588 as N
		,N'РасчетСебестоимостиТоваров' as Имя
		,N'Расчет себестоимости товаров' as Синоним
	union all select
		589 as N
		,N'РеализацияБезПереходаПраваСобственности' as Имя
		,N'Реализация (товары в пути)' as Синоним
	union all select
		590 as N
		,N'РеализацияВнеоборотныхАктивов' as Имя
		,N'Реализация внеоборотных активов' as Синоним
	union all select
		591 as N
		,N'РеализацияВРозницу' as Имя
		,N'Реализация в розницу' as Синоним
	union all select
		592 as N
		,N'РеализацияКлиенту' as Имя
		,N'Реализация' as Синоним
	union all select
		593 as N
		,N'РеализацияКлиентуРеглУчет' as Имя
		,N'Реализация (только регл. учет)' as Синоним
	union all select
		594 as N
		,N'РеализацияКомиссионногоТовара' as Имя
		,N'Реализация комиссионного товара' as Синоним
	union all select
		595 as N
		,N'РеализацияНМА' as Имя
		,N'Реализация НМА и НИОКР' as Синоним
	union all select
		596 as N
		,N'РеализацияОС' as Имя
		,N'Реализация основных средств' as Синоним
	union all select
		597 as N
		,N'РеализацияОСсОтложеннымПереходомПрав' as Имя
		,N'Реализация ОС с отложенным переходом прав' as Синоним
	union all select
		598 as N
		,N'РеализацияПереданнойВозвратнойТары' as Имя
		,N'Реализация переданной возвратной тары' as Синоним
	union all select
		599 as N
		,N'РеализацияПерепоставленногоТовара' as Имя
		,N'Реализация перепоставленного товара' as Синоним
	union all select
		600 as N
		,N'РеализацияПодарочныхСертификатов' as Имя
		,N'Реализация подарочных сертификатов' as Синоним
	union all select
		601 as N
		,N'РеализацияПрочихАктивов' as Имя
		,N'Реализация прочих активов' as Синоним
	union all select
		602 as N
		,N'РеализацияПрочихУслуг' as Имя
		,N'Реализация прочих услуг' as Синоним
	union all select
		603 as N
		,N'РеализацияТоваровВДругуюОрганизацию' as Имя
		,N'Реализация товаров в другую организацию' as Синоним
	union all select
		604 as N
		,N'РеализацияЧерезКомиссионера' as Имя
		,N'Реализация через комиссионера' as Синоним
	union all select
		605 as N
		,N'РеализацияЧерезКомиссионераБезПереходаПраваСобственности' as Имя
		,N'Реализация через комиссионера (товары в пути)' as Синоним
	union all select
		606 as N
		,N'РегистрацияДефекта' as Имя
		,N'Регистрация дефекта' as Синоним
	union all select
		607 as N
		,N'РегистрацияРасходовУУ' as Имя
		,N'Регистрация расходов в упр. учете' as Синоним
	union all select
		608 as N
		,N'РегистрацияСдельныхРабот' as Имя
		,N'Регистрация сдельных работ' as Синоним
	union all select
		609 as N
		,N'РегламентнаяОперация' as Имя
		,N'Регламентная операция' as Синоним
	union all select
		610 as N
		,N'РегламентнаяОперацияМеждународныйУчет' as Имя
		,N'Регламентная операция международный учет' as Синоним
	union all select
		611 as N
		,N'РезервированиеАвансаКлиента' as Имя
		,N'Резервирование аванса клиента' as Синоним
	union all select
		612 as N
		,N'РеклассификацияДолгосрочныхАктивовОбязательств' as Имя
		,N'Реклассификация долгосрочных активов и обязательств' as Синоним
	union all select
		613 as N
		,N'РеклассификацияДоходов' as Имя
		,N'Реклассификация доходов' as Синоним
	union all select
		614 as N
		,N'РеклассификацияНМА' as Имя
		,N'Реклассификация (изменение параметров) НМА' as Синоним
	union all select
		615 as N
		,N'РеклассификацияОС' as Имя
		,N'Реклассификация (изменение параметров) ОС' as Синоним
	union all select
		616 as N
		,N'РеклассификацияРасходов' as Имя
		,N'Реклассификация расходов' as Синоним
	union all select
		617 as N
		,N'Ремонт' as Имя
		,N'Ремонт' as Синоним
	union all select
		618 as N
		,N'СборкаТоваров' as Имя
		,N'Сборка из комплектующих' as Синоним
	union all select
		619 as N
		,N'СдачаДенежныхСредствВБанк' as Имя
		,N'Сдача ДС в банк' as Синоним
	union all select
		620 as N
		,N'СебестоимостьРеализацииНМА' as Имя
		,N'Себестоимость реализации НМА' as Синоним
	union all select
		621 as N
		,N'СебестоимостьРеализацииОС' as Имя
		,N'Себестоимость реализации ОС' as Синоним
	union all select
		622 as N
		,N'СнятиеНаличныхДенежныхСредств' as Имя
		,N'Инкассация ДС из банка в кассу' as Синоним
	union all select
		623 as N
		,N'СнятиеСРегистрацииЗемельныхУчастков' as Имя
		,N'Снятие с регистрации земельных участков' as Синоним
	union all select
		624 as N
		,N'СнятиеСРегистрацииТранспортныхСредств' as Имя
		,N'Снятие с регистрации транспортных средств' as Синоним
	union all select
		625 as N
		,N'СобственноеПроизводство' as Имя
		,N'Собственное производство' as Синоним
	union all select
		626 as N
		,N'СписаниеАмортизацииНМА' as Имя
		,N'Списание амортизации НМА' as Синоним
	union all select
		627 as N
		,N'СписаниеАмортизацииОС' as Имя
		,N'Списание амортизации ОС' as Синоним
	union all select
		628 as N
		,N'СписаниеБезнадежнойЗадолженностиЗаСчетРезервовПоСомнительнымДолгам' as Имя
		,N'Списание безнадежной задолженности за счет резервов по сомнительным долгам' as Синоним
	union all select
		629 as N
		,N'СписаниеДебиторскойЗадолженности' as Имя
		,N'Списание дебиторской задолженности' as Синоним
	union all select
		630 as N
		,N'СписаниеДебиторскойЗадолженностиНаАктивыПассивы' as Имя
		,N'Списание дебиторской задолженности на активы \ пассивы' as Синоним
	union all select
		631 as N
		,N'СписаниеДебиторскойЗадолженностиНаРасходы' as Имя
		,N'Списание дебиторской задолженности на расходы' as Синоним
	union all select
		632 as N
		,N'СписаниеДенежныхДокументов' as Имя
		,N'Списание денежных документов' as Синоним
	union all select
		633 as N
		,N'СписаниеЗалоговойСтоимостиАрендованныхОС' as Имя
		,N'Списание залоговой стоимости арендованных ОС' as Синоним
	union all select
		634 as N
		,N'СписаниеИзЭксплуатации' as Имя
		,N'Списание из эксплуатации' as Синоним
	union all select
		635 as N
		,N'СписаниеКомиссионныхТоваров' as Имя
		,N'Списание комиссионных товаров' as Синоним
	union all select
		636 as N
		,N'СписаниеКосвенныхРасходов' as Имя
		,N'Списание косвенных расходов' as Синоним
	union all select
		637 as N
		,N'СписаниеКредиторскойЗадолженности' as Имя
		,N'Списание кредиторской задолженности' as Синоним
	union all select
		638 as N
		,N'СписаниеКредиторскойЗадолженностиВДоходы' as Имя
		,N'Списание кредиторской задолженности в доходы' as Синоним
	union all select
		639 as N
		,N'СписаниеНаРасходыМалоценныхТМЦВМесяцеПриобретения' as Имя
		,N'Списание на расходы малоценных ТМЦ в месяце приобретения' as Синоним
	union all select
		640 as N
		,N'СписаниеНаРасходыНИОКР' as Имя
		,N'Списание на расходы НИОКР' as Синоним
	union all select
		641 as N
		,N'СписаниеНаРасходыНИОКРВДругуюОрганизацию' as Имя
		,N'Списание на расходы НИОКР в другую организацию' as Синоним
	union all select
		642 as N
		,N'СписаниеНаРасходыНИОКРИзДругойОрганизации' as Имя
		,N'Списание на расходы НИОКР из другой организации' as Синоним
	union all select
		643 as N
		,N'СписаниеНаРасходыСтоимостиНМАНеПринимаяКУчету' as Имя
		,N'Списание на расходы стоимости НМА (не принимая к учету)' as Синоним
	union all select
		644 as N
		,N'СписаниеНаРасходыСтоимостиОСНеПринимаяКУчету' as Имя
		,N'Списание на расходы стоимости ОС (не принимая к учету)' as Синоним
	union all select
		645 as N
		,N'СписаниеНаРасходыФиксированнаяСтоимость' as Имя
		,N'Списание на расходы (фиксированная стоимость)' as Синоним
	union all select
		646 as N
		,N'СписаниеНДСПоАренде' as Имя
		,N'Списание НДС по аренде' as Синоним
	union all select
		647 as N
		,N'СписаниеНДСПоПриобретеннымЦенностям' as Имя
		,N'Списание НДС по приобретенным ценностям' as Синоним
	union all select
		648 as N
		,N'СписаниеНДССПолученногоАванса' as Имя
		,N'Списание НДС с полученного аванса' as Синоним
	union all select
		649 as N
		,N'СписаниеНедостачЗаСчетКомитента' as Имя
		,N'Списание недостач за счет комитента' as Синоним
	union all select
		650 as N
		,N'СписаниеНедостачЗаСчетПоклажедателя' as Имя
		,N'Списание недостач за счет поклажедателя' as Синоним
	union all select
		651 as N
		,N'СписаниеНеУчитываемойСтоимостиНУ' as Имя
		,N'Списание не учитываемой стоимости НУ' as Синоним
	union all select
		652 as N
		,N'СписаниеНМА' as Имя
		,N'Списание НМА' as Синоним
	union all select
		653 as N
		,N'СписаниеНМАЧастичное' as Имя
		,N'Частичное списание НМА' as Синоним
	union all select
		654 as N
		,N'СписаниеОбесцененияНМА' as Имя
		,N'Списание обесценения НМА' as Синоним
	union all select
		655 as N
		,N'СписаниеОбесцененияОС' as Имя
		,N'Списание обесценения ОС' as Синоним
	union all select
		656 as N
		,N'СписаниеОС' as Имя
		,N'Списание ОС' as Синоним
	union all select
		657 as N
		,N'СписаниеОСпоИнвентаризации' as Имя
		,N'Списание ОС по инвентаризации' as Синоним
	union all select
		658 as N
		,N'СписаниеОСЧастичное' as Имя
		,N'Частичное списание ОС' as Синоним
	union all select
		659 as N
		,N'СписаниеОшибокОкругления' as Имя
		,N'Списание ошибок округления' as Синоним
	union all select
		660 as N
		,N'СписаниеОшибокОкругленияВозвратныеОтходы' as Имя
		,N'Списание ошибок округления (стоимость возвратных отходов в производстве)' as Синоним
	union all select
		661 as N
		,N'СписаниеПринятыхТоваровЗаСчетПоклажедателя' as Имя
		,N'Списание принятых товаров за счет поклажедателя' as Синоним
	union all select
		662 as N
		,N'СписаниеПринятыхТоваровНаРасходы' as Имя
		,N'Списание принятых товаров на расходы' as Синоним
	union all select
		663 as N
		,N'СписаниеПроцентовПоАренде' as Имя
		,N'Списание процентов по аренде' as Синоним
	union all select
		664 as N
		,N'СписаниеПроцентовПоДисконтированию' as Имя
		,N'Списание процентов по дисконтированию' as Синоним
	union all select
		665 as N
		,N'СписаниеПрочихДоходов' as Имя
		,N'Списание прочих доходов' as Синоним
	union all select
		666 as N
		,N'СписаниеПрочихРасходов' as Имя
		,N'Списание прочих расходов' as Синоним
	union all select
		667 as N
		,N'СписаниеРасходовЗаСчетРезервов' as Имя
		,N'Списание расходов за счет резервов' as Синоним
	union all select
		668 as N
		,N'СписаниеРасходовНаПартииПроизводства' as Имя
		,N'Списание расходов на партии производства' as Синоним
	union all select
		669 as N
		,N'СписаниеРезерваПереоценкиАмортизацииНМА' as Имя
		,N'Списание резерва переоценки амортизации НМА' as Синоним
	union all select
		670 as N
		,N'СписаниеРезерваПереоценкиАмортизацииОС' as Имя
		,N'Списание резерва переоценки амортизации ОС' as Синоним
	union all select
		671 as N
		,N'СписаниеРезерваПереоценкиСтоимостиНМА' as Имя
		,N'Списание резерва переоценки стоимости НМА' as Синоним
	union all select
		672 as N
		,N'СписаниеРезерваПереоценкиСтоимостиОС' as Имя
		,N'Списание резерва переоценки стоимости ОС' as Синоним
	union all select
		673 as N
		,N'СписаниеРезервовПодОбесценениеЗапасов' as Имя
		,N'Списание резервов под обесценение запасов' as Синоним
	union all select
		674 as N
		,N'СписаниеРезервовПредстоящихРасходов' as Имя
		,N'Списание резервов предстоящих расходов' as Синоним
	union all select
		675 as N
		,N'СписаниеСтоимостиАрендованныхОС' as Имя
		,N'Списание стоимости арендованных ОС' as Синоним
	union all select
		676 as N
		,N'СписаниеСтоимостиНМА' as Имя
		,N'Списание стоимости НМА' as Синоним
	union all select
		677 as N
		,N'СписаниеСтоимостиОС' as Имя
		,N'Списание стоимости ОС' as Синоним
	union all select
		678 as N
		,N'СписаниеТоваров' as Имя
		,N'Списание товаров' as Синоним
	union all select
		679 as N
		,N'СписаниеТоваровДавальцаЗаСчетДавальца' as Имя
		,N'Списание товаров давальца за счет давальца' as Синоним
	union all select
		680 as N
		,N'СписаниеТоваровДавальцаНаРасходы' as Имя
		,N'Списание товаров давальца на расходы' as Синоним
	union all select
		681 as N
		,N'СписаниеТоваровПоТребованию' as Имя
		,N'Списание на расходы' as Синоним
	union all select
		682 as N
		,N'СписаниеТоваровСХранения' as Имя
		,N'Списание товаров с хранения' as Синоним
	union all select
		683 as N
		,N'СписаниеТоваровУКомиссионера' as Имя
		,N'Списание товаров у комиссионера' as Синоним
	union all select
		684 as N
		,N'СписаниеТоваровУПереработчика' as Имя
		,N'Списание товаров у переработчика' as Синоним
	union all select
		685 as N
		,N'СписаниеУзловКомпонентовАмортизации' as Имя
		,N'Списание узлов и компонентов амортизации' as Синоним
	union all select
		686 as N
		,N'СторнированиеПрочихДоходов' as Имя
		,N'Сторнирование прочих доходов' as Синоним
	union all select
		687 as N
		,N'СторнированиеПрочихРасходов' as Имя
		,N'Сторнирование прочих расходов' as Синоним
	union all select
		688 as N
		,N'СторнированиеРасходовУУ' as Имя
		,N'Сторнирование расходов в упр. учете' as Синоним
	union all select
		689 as N
		,N'СторноОбесцененияНИОКР' as Имя
		,N'Сторно обесценения НИОКР' as Синоним
	union all select
		690 as N
		,N'СторноОбесцененияНИОКРВДругуюОрганизацию' as Имя
		,N'Сторно обесценения НИОКР в другую организацию' as Синоним
	union all select
		691 as N
		,N'СторноОбесцененияНИОКРИзДругойОрганизации' as Имя
		,N'Сторно обесценения НИОКР из другой организации' as Синоним
	union all select
		692 as N
		,N'СторноОбесцененияНМА' as Имя
		,N'Сторно обесценения НМА' as Синоним
	union all select
		693 as N
		,N'СторноОбесцененияНМАВДругуюОрганизацию' as Имя
		,N'Сторно обесценения НМА в другую организацию' as Синоним
	union all select
		694 as N
		,N'СторноОбесцененияНМАИзДругойОрганизации' as Имя
		,N'Сторно обесценения НМА из другой организации' as Синоним
	union all select
		695 as N
		,N'СторноОбесцененияОС' as Имя
		,N'Сторно обесценения ОС' as Синоним
	union all select
		696 as N
		,N'СторноОбесцененияОСВДругуюОрганизацию' as Имя
		,N'Сторно обесценения ОС в другую организацию' as Синоним
	union all select
		697 as N
		,N'СторноОбесцененияОСИзДругойОрганизации' as Имя
		,N'Сторно обесценения ОС из другой организации' as Синоним
	union all select
		698 as N
		,N'СторноПереданнойТары' as Имя
		,N'Сторно переданной тары' as Синоним
	union all select
		699 as N
		,N'СторноПереданнойТарыВозвратНаДругойСклад' as Имя
		,N'Сторно переданной тары (возврат на другой склад)' as Синоним
	union all select
		700 as N
		,N'СторноПоступления' as Имя
		,N'Сторно поступления' as Синоним
	union all select
		701 as N
		,N'СторноПроизводственныхЗатрат' as Имя
		,N'Сторно производственных затрат' as Синоним
	union all select
		702 as N
		,N'СторноРеализации' as Имя
		,N'Сторно реализации' as Синоним
	union all select
		703 as N
		,N'СторноРеализацииВозвратНаДругойСклад' as Имя
		,N'Сторно реализации (возврат на другой склад)' as Синоним
	union all select
		704 as N
		,N'СторноСписанияНаРасходы' as Имя
		,N'Сторно списания на расходы' as Синоним
	union all select
		705 as N
		,N'ТранзитРасходовМеждуОВЗ' as Имя
		,N'Транзит расходов между объектами возникновения затрат' as Синоним
	union all select
		706 as N
		,N'УвеличениеНакопленнойАмортизацииНМА' as Имя
		,N'Увеличение накопленной амортизации НМА' as Синоним
	union all select
		707 as N
		,N'УвеличениеНакопленнойАмортизацииОС' as Имя
		,N'Увеличение накопленной амортизации ОС' as Синоним
	union all select
		708 as N
		,N'УвеличениеНДСПоАренде' as Имя
		,N'Увеличение НДС по аренде' as Синоним
	union all select
		709 as N
		,N'УвеличениеПроцентовПоАренде' as Имя
		,N'Увеличение процентов по аренде' as Синоним
	union all select
		710 as N
		,N'УвеличениеСтоимостиАрендованныхОС' as Имя
		,N'Увеличение стоимости арендованных ОС' as Синоним
	union all select
		711 as N
		,N'УвеличениеСтоимостиНМА' as Имя
		,N'Увеличение стоимости НМА' as Синоним
	union all select
		712 as N
		,N'УвеличениеСтоимостиОС' as Имя
		,N'Увеличение стоимости ОС' as Синоним
	union all select
		713 as N
		,N'УдалитьСписаниеТоваровПереданныхПартнерам' as Имя
		,N'(Не используется) Списание товаров, переданных партнерам' as Синоним
	union all select
		714 as N
		,N'УдержаниеВознагражденияКомиссионера' as Имя
		,N'Удержание вознаграждения комиссионера' as Синоним
	union all select
		715 as N
		,N'УдержаниеВознагражденияКомитентом' as Имя
		,N'Удержание вознаграждения комитентом' as Синоним
	union all select
		716 as N
		,N'УдержаниеИзЗарплатыВСчетРеализацииСотруднику' as Имя
		,N'Удержание из зарплаты в счет реализации сотруднику' as Синоним
	union all select
		717 as N
		,N'УдержаниеИзЗарплатыСотрудника' as Имя
		,N'Удержание из зарплаты сотрудника' as Синоним
	union all select
		718 as N
		,N'УдержаниеНеизрасходованныхПодотчетныхСумм' as Имя
		,N'Удержание неизрасходованных подотчетных сумм' as Синоним
	union all select
		719 as N
		,N'УлучшениеНМА' as Имя
		,N'Улучшение НМА' as Синоним
	union all select
		720 as N
		,N'УменьшениеВеличиныДооценкиНакопленнойАмортизацииНМА' as Имя
		,N'Уменьшение величины дооценки накопленной амортизации НМА' as Синоним
	union all select
		721 as N
		,N'УменьшениеВеличиныДооценкиНакопленнойАмортизацииОС' as Имя
		,N'Уменьшение величины дооценки накопленной амортизации ОС' as Синоним
	union all select
		722 as N
		,N'УменьшениеВеличиныДооценкиСтоимостиНМА' as Имя
		,N'Уменьшение величины дооценки стоимости НМА' as Синоним
	union all select
		723 as N
		,N'УменьшениеВеличиныДооценкиСтоимостиОС' as Имя
		,N'Уменьшение величины дооценки стоимости ОС' as Синоним
	union all select
		724 as N
		,N'УменьшениеНакопленнойАмортизацииНМА' as Имя
		,N'Уменьшение накопленной амортизации НМА' as Синоним
	union all select
		725 as N
		,N'УменьшениеНакопленнойАмортизацииОС' as Имя
		,N'Уменьшение накопленной амортизации ОС' as Синоним
	union all select
		726 as N
		,N'УменьшениеНДСПоАренде' as Имя
		,N'Уменьшение НДС по аренде' as Синоним
	union all select
		727 as N
		,N'УменьшениеПроцентовПоАренде' as Имя
		,N'Уменьшение процентов по аренде' as Синоним
	union all select
		728 as N
		,N'УменьшениеСтоимостиАрендованныхОС' as Имя
		,N'Уменьшение стоимости арендованных ОС' as Синоним
	union all select
		729 as N
		,N'УменьшениеСтоимостиНМА' as Имя
		,N'Уменьшение стоимости НМА' as Синоним
	union all select
		730 as N
		,N'УменьшениеСтоимостиОС' as Имя
		,N'Уменьшение стоимости ОС' as Синоним
	union all select
		731 as N
		,N'УстановкаЗначенийНаработки' as Имя
		,N'Установка значений наработки' as Синоним
	union all select
		732 as N
		,N'ФормированиеСтоимостиАрендованныхОС' as Имя
		,N'Формирование стоимости арендованных ОС' as Синоним
	union all select
		733 as N
		,N'ШтрафыПриВозвратеБронирования' as Имя
		,N'Штрафы при возврате бронирования' as Синоним
	union all select
		734 as N
		,N'ШтрафыПриВозвратеБронированияПодотчетногоЛица' as Имя
		,N'Штрафы при возврате бронирования подотчетного лица' as Синоним
	) S on S.N=_Enum3172._EnumOrder
) hoz_operacii on hoz_operacii._IDRRef = registr_sebes._Fld92775RRef
left join (
select
vtr_potr.[_IDRRef] as DocID,
case 
	when monitor.Elt_bn is not null then monitor.Elt_bn
	when seria.[_Description] != 'Техническая' then seria.[_Description]
	when seria.[_Description] = 'Техническая' then seria.[_Description] 
	else null
end as elt_bn_,
cast(dateadd(year,-2000,vtr_potr.[_Date_Time]) as date) as Period,
vtr_potr.[_Number] as NumberDoc1C,
orderfrom.[_Description] as OrderOut,
nomen.IDnomen,
nomen.Nomen_Code,
nomen.Nomen_pn,
nomen.[Nomen_name] as Nomenklatura,
vtr_potr_tovar.[_LineNo9190] as Item_SO,
vtr_potr_tovar._Fld9199 as Qty_SO,
seria.[_Description] as Seria,
monitor.Elt_bn,
monitor.StatusOperation,
monitor.SO_Number,
objectexpl.[_Description] as ObjectExpl
from _Document1178 vtr_potr
left join _Document1178_VT9189 vtr_potr_tovar on vtr_potr_tovar.[_Document1178_IDRRef] = vtr_potr.[_IDRRef]
left join _Reference848 orderfrom on orderfrom.[_IDRRef] = vtr_potr.[_Fld9168RRef]
left join _Reference836 seria on seria.[_IDRRef] = vtr_potr_tovar.[_Fld9196RRef]
left join _Reference558 objectexpl on objectexpl.[_IDRRef] = vtr_potr_tovar._Fld9201_RRRef
left join (
select
t1.IDnomen as IDnomen,
t1.Код as Nomen_Code,
t1.[Наименование] as Nomen_name,
t1.[Партийный номер (Сырье и материалы 10 01 ТД)] as Nomen_pn
from (
select *
from (
select
	_Reference539._IDRRef as IDnomen
	,IIF(_Reference539._Marked<>'','Удалено','Не_удалено') as ПометкаУдаления
	,_Reference539._Code as Код
	,_Fld55631 as Артикул
	,_Reference290._Description as ГруппаДоступа
	,_Reference539._Description as Наименование
	,_Reference221._Description as ВидНоменклатуры
	,_Chrc3194._Description as name_
	,_Fld55734_S as value
from dbo._Reference539
join dbo._Reference539_VT55731 on dbo._Reference539_VT55731._Reference539_IDRRef = dbo._Reference539._IDRRef
join dbo._Chrc3194 on dbo._Chrc3194._IDRRef = dbo._Reference539_VT55731._Fld55733RRef
left join dbo._Reference290 on dbo._Reference290._IDRRef = _Fld55642RRef
left join dbo._Reference221 on dbo._Reference221._IDRRef = _Fld55641RRef
left join dbo._InfoRg87665 on dbo._InfoRg87665._Fld87667RRef = dbo._Reference539.[_IDRRef] 
) src
pivot (max([value]) for [name_] in ([Код АСУ НСИ],[Guid КУПОЛ],[Партийный номер (Сырье и материалы 10 01 ТД)],[Тип номенклатуры (Сырье и материалы 10 01 ТД)])) as pvt
)t1
where t1.[Партийный номер (Сырье и материалы 10 01 ТД)] is not null
) nomen on nomen.IDnomen = vtr_potr_tovar.[_Fld9194RRef]
left join (
select
cast(dateadd(year,-2000,monitor.[_Fld96619]) as date) as Period,
RIGHT(monitor.[_Number],(LEN(monitor.[_Number])-CHARINDEX('-',monitor.[_Number],4))) as SO_Number,
status_operation.[_EnumOrder] as StatusOperation,
monitor.[_Fld96623] as TextError,
monitor_tovar.[_Fld96639] as Qty_monitor,
monitor_tovar.[_Fld96646] as Elt_bn,
monitor_tovar.[_LineNo96636] as Item_monitor,
monitor._Fld96622_RRRef as Doc1cId
from _Document96611 monitor
left join (
select
_IDRRef as _IDRRef,
case
	when _EnumOrder = 0 then 'Приемка'
	when _EnumOrder = 1 then 'Размещение'
	when _EnumOrder = 2 then 'Выбытие'
	when _EnumOrder = 3 then 'Перемещение'
	when _EnumOrder = 4 then 'Возврат'
	when _EnumOrder = 5 then 'Заказ'
	when _EnumOrder = 6 then 'Снятие с ВС'
end as _EnumOrder
from _Enum1759
) type_operation on type_operation.[_IDRRef] = monitor._Fld96612RRef
left join (
select
_IDRRef as _IDRRef,
case 
	when _EnumOrder = 0 then 'Загружен'
	when _EnumOrder = 1 then 'В обработке'
	when _EnumOrder = 2 then 'Обработан'
	when _EnumOrder = 3 then 'Отражен в регл. учете'
	when _EnumOrder = 4 then 'Не требует обработки'
	when _EnumOrder = 5 then 'Ошибка'
end as _EnumOrder
from _Enum1781
) status_operation on status_operation.[_IDRRef] = monitor._Fld96621RRef
left join _Document96611_VT96635 monitor_tovar on monitor_tovar.[_Document96611_IDRRef] = monitor.[_IDRRef]
where iif([_Marked]<>'',1,0)=0 and type_operation._EnumOrder = 'Выбытие'
) monitor on monitor.Doc1cId = vtr_potr.[_IDRRef] and monitor.Item_monitor = vtr_potr_tovar.[_LineNo9190]
where iif(vtr_potr._Marked<>'',1,0)=0 and seria.[_Description] is not null
/*union all
select
prochee.[_IDRRef] as DocID,
case 
	when monitor.Elt_bn is not null then monitor.Elt_bn
	when seria.[_Description] != 'Техническая' then seria.[_Description]
	when seria.[_Description] = 'Техническая' then seria.[_Description] 
	else null
end as elt_bn_,
cast(dateadd(year,-2000,prochee.[_Date_Time]) as date) as Period,
prochee.[_Number] as NumberDoc1c,
orderfrom.[_Description] as OrderOut,
nomen.IDnomen,
nomen.Nomen_Code,
nomen.Nomen_pn,
nomen.[Nomen_name] as Nomenklatura,
prochee_tovar.[_LineNo34615] as Item_SO,
prochee_tovar._Fld34621 as Qty_SO,
seria.[_Description] as Seria,
monitor.Elt_bn,
monitor.StatusOperation,
monitor.ISR_Number,
objectexpl.[_Description] as ObjectExpl
from _Document1553 prochee
left join _Document1553_VT34614 prochee_tovar on prochee_tovar.[_Document1553_IDRRef] = prochee.[_IDRRef]
left join _Reference848 orderfrom on orderfrom.[_IDRRef] = prochee.[_Fld34599RRef]
left join _Reference836 seria on seria.[_IDRRef] = prochee_tovar.[_Fld34630RRef]
left join _Reference558 objectexpl on objectexpl.[_IDRRef] = prochee_tovar._Fld34626_RRRef
left join (
select
t1.IDnomen as IDnomen,
t1.Код as Nomen_Code,
t1.[Наименование] as Nomen_name,
t1.[Партийный номер (Сырье и материалы 10 01 ТД)] as Nomen_pn
from (
select *
from (
select
	_Reference539._IDRRef as IDnomen
	,IIF(_Reference539._Marked<>'','Удалено','Не_удалено') as ПометкаУдаления
	,_Reference539._Code as Код
	,_Fld55631 as Артикул
	,_Reference290._Description as ГруппаДоступа
	,_Reference539._Description as Наименование
	,_Reference221._Description as ВидНоменклатуры
	,_Chrc3194._Description as name_
	,_Fld55734_S as value
from dbo._Reference539
join dbo._Reference539_VT55731 on dbo._Reference539_VT55731._Reference539_IDRRef = dbo._Reference539._IDRRef
join dbo._Chrc3194 on dbo._Chrc3194._IDRRef = dbo._Reference539_VT55731._Fld55733RRef
left join dbo._Reference290 on dbo._Reference290._IDRRef = _Fld55642RRef
left join dbo._Reference221 on dbo._Reference221._IDRRef = _Fld55641RRef
left join dbo._InfoRg87665 on dbo._InfoRg87665._Fld87667RRef = dbo._Reference539.[_IDRRef] 
) src
pivot (max([value]) for [name_] in ([Код АСУ НСИ],[Guid КУПОЛ],[Партийный номер (Сырье и материалы 10 01 ТД)],[Тип номенклатуры (Сырье и материалы 10 01 ТД)])) as pvt
)t1
where t1.[Партийный номер (Сырье и материалы 10 01 ТД)] is not null
) nomen on nomen.IDnomen = prochee_tovar._Fld34617RRef
left join (
select
cast(dateadd(year,-2000,monitor.[_Fld96619]) as date) as Period,
right(monitor.[_Number],5) as ISR_Number,
status_operation.[_EnumOrder] as StatusOperation,
monitor.[_Fld96623] as TextError,
monitor_tovar.[_Fld96639] as Qty_monitor,
monitor_tovar.[_Fld96646] as Elt_bn,
monitor_tovar.[_LineNo96636] as Item_monitor,
monitor._Fld96622_RRRef as Doc1cId
from _Document96611 monitor
left join (
select
_IDRRef as _IDRRef,
case
	when _EnumOrder = 0 then 'Приемка'
	when _EnumOrder = 1 then 'Размещение'
	when _EnumOrder = 2 then 'Выбытие'
	when _EnumOrder = 3 then 'Перемещение'
	when _EnumOrder = 4 then 'Возврат'
	when _EnumOrder = 5 then 'Заказ'
	when _EnumOrder = 6 then 'Снятие с ВС'
end as _EnumOrder
from _Enum1759
) type_operation on type_operation.[_IDRRef] = monitor._Fld96612RRef
left join (
select
_IDRRef as _IDRRef,
case 
	when _EnumOrder = 0 then 'Загружен'
	when _EnumOrder = 1 then 'В обработке'
	when _EnumOrder = 2 then 'Обработан'
	when _EnumOrder = 3 then 'Отражен в регл. учете'
	when _EnumOrder = 4 then 'Не требует обработки'
	when _EnumOrder = 5 then 'Ошибка'
end as _EnumOrder
from _Enum1781
) status_operation on status_operation.[_IDRRef] = monitor._Fld96621RRef
left join _Document96611_VT96635 monitor_tovar on monitor_tovar.[_Document96611_IDRRef] = monitor.[_IDRRef]
where iif([_Marked]<>'',1,0)=0 and type_operation._EnumOrder = 'Выбытие'
) monitor on monitor.Doc1cId = prochee.[_IDRRef] and monitor.Item_monitor = prochee_tovar.[_LineNo34615]
left join _Enum3172 hoz on hoz.[_IDRRef] = prochee.[_Fld34604RRef]
where iif(prochee._Marked<>'',1,0)=0 and seria.[_Description] is not null and hoz.[_EnumOrder] = 696*/
) monitor on monitor.DocID = registr_sebes._RecorderRRef and monitor.IDnomen = nomenklatura.IDnomen and monitor.seria = seria.[_Description] and monitor.ObjectExpl = (IIF(object_rashod._Description is not null, object_rashod._Description, 
IIF(partners_analitika._Description is not null, partners_analitika._Description,
IIF(nd_analitika._Description is not null, nd_analitika._Description, 
registr_sebes._Fld92784_RRRef))))
where cast(dateadd(year,-2000,registr_sebes.[_Period]) as date) >= '2023-03-01' and registr_sebes._Fld92749 not in (0)
and (hoz_operacii.Синоним = 'Передача в состав основных средств' or hoz_operacii.Синоним = 'Списание на расходы' or hoz_operacii.Синоним = 'Передача переработчику' or hoz_operacii.Синоним = 'Реализация' or hoz_operacii.Синоним = 'Возврат товаров поставщику'
or hoz_operacii.Синоним = 'Сторно списания на расходы')
and seria.[_Description] is not null
and iif(registr_sebes._RecordKind=1,'Списание','Поступление') = 'Списание'
and (case 
	when monitor.elt_bn_ is null then seria.[_Description]
	else monitor.elt_bn_
end) is not null
and hoz_operacii_spis.Имя is null
--gtd_number = '10005030/220722/3198640' and nomenklatura.Nomen_pn = 'BACS12HM08AH10' and 
--and hoz_operacii.[Синоним] <> 'Перемещение товаров'
group by 
case 
	when ptu_registr._Number is not null then 'Приобретение товаров и услуг ' + ptu_registr._Number
	when spis_registr._Number is not null then 'Списание на расходы ' + spis_registr._Number
 	when vozvrat_tovarov._Number is not null then 'Возврат товаров поставщику ' + vozvrat_tovarov._Number
	when peremestit._Number is not null then 'Перемещение товаров ' + peremestit._Number
	when storno_spis._Number is not null then 'Сторно списания на расходы ' + storno_spis._Number
	when peredacha._Number is not null then 'Передача переработчику ' + peredacha._Number
	when vozvrat_siria._Number is not null then 'Возврат от переработчика ' + vozvrat_siria._Number
	when sborka_razborka._Number is not null then 'Сборка (разборка) товаров ' + sborka_razborka._Number
	when realiazcia._Number is not null then 'Реализация товаров и услуг ' + realiazcia._Number
	when otvet_hranenie._Number is not null then 'Приемка товаров на хранение' + otvet_hranenie._Number
	when peredacha_hranitel._Number is not null then 'Передача на ответ хранение' + peredacha_hranitel._Number
	else registr_sebes._RecorderRRef
end,
case	
	when ptu_registr._Number is not null then 'Приобретение товаров и услуг'
	when spis_registr._Number is not null then 'Списание на расходы'
 	when vozvrat_tovarov._Number is not null then 'Возврат товаров поставщику'
	when peremestit._Number is not null then 'Перемещение товаров'
	when storno_spis._Number is not null then 'Сторно списания на расходы'
	when peredacha._Number is not null then 'Передача переработчику'
	when vozvrat_siria._Number is not null then 'Возврат от переработчика'
	when sborka_razborka._Number is not null then 'Сборка (разборка) товаров'
	when realiazcia._Number is not null then 'Реализация товаров и услуг'
	when otvet_hranenie._Number is not null then 'Приемка товаров на хранение' 
	when peredacha_hranitel._Number is not null then 'Передача на ответ хранение'
	else registr_sebes._RecorderRRef
end,
case 
	when ptu_registr._Number is not null then ptu_registr._Number
	when spis_registr._Number is not null then spis_registr._Number
 	when vozvrat_tovarov._Number is not null then  vozvrat_tovarov._Number
	when peremestit._Number is not null then peremestit._Number
	when storno_spis._Number is not null then storno_spis._Number
	when peredacha._Number is not null then peredacha._Number
	when vozvrat_siria._Number is not null then vozvrat_siria._Number
	when sborka_razborka._Number is not null then sborka_razborka._Number
	when realiazcia._Number is not null then realiazcia._Number
	when otvet_hranenie._Number is not null then otvet_hranenie._Number
	when peredacha_hranitel._Number is not null then peredacha_hranitel._Number
	else registr_sebes._RecorderRRef
end,
gtds.gtd_number,
/*iif(ptu._Number is not null, ptu._Number, 
iif(otvet_hranenie_partia._Number is not null, otvet_hranenie_partia._Number,
registr_sebes._Fld92745_RRRef)),*/
cast(dateadd(year,-2000,registr_sebes._Period) as date),
nomenklatura.Nomen_code,
nomenklatura.Nomen_name,
nomenklatura.Nomen_pn,
monitor.SO_Number,
case 
	when monitor.elt_bn_ is null then seria.[_Description]
	else monitor.elt_bn_
end,
--seria.[_Description],
--monitor.elt_bn_,
--registr_sebes._Fld92749,
--iif(registr_sebes._RecordKind=1,registr_sebes._Fld92749*-1,registr_sebes._Fld92749),
--registr_sebes._Fld92760,
iif(registr_sebes._RecordKind=1,'Списание','Поступление'),
hoz_operacii.[Синоним],
orders._Description,
IIF(object_rashod._Description is not null, object_rashod._Description, 
IIF(partners_analitika._Description is not null, partners_analitika._Description,
IIF(nd_analitika._Description is not null, nd_analitika._Description, 
registr_sebes._Fld92784_RRRef))),
right(IIF(object_rashod._Description is not null, object_rashod._Description, 
IIF(partners_analitika._Description is not null, partners_analitika._Description,
IIF(nd_analitika._Description is not null, nd_analitika._Description, 
registr_sebes._Fld92784_RRRef))),8),
partners._Description,
case 
	when cast(dateadd(year,-2000,registr_sebes._Period) as date) <= '2023-03-13' then 'Дата документа меньше, чем 14.03'
	else null
end,
case 
	when users_ptu._Description is not null then users_ptu._Description
	when users_spis_registr._Description is not null then users_spis_registr._Description
	when users_vozvrat_tovarov._Description is not null then users_vozvrat_tovarov._Description
	when users_peremestit._Description is not null then users_peremestit._Description
	when users_storno_spis._Description is not null then users_storno_spis._Description
	when users_peredacha._Description is not null then users_peredacha._Description
	when users_vozvrat_siria._Description is not null then users_vozvrat_siria._Description
	when users_sborka_razborka._Description is not null then users_sborka_razborka._Description
	when users_realiazcia._Description is not null then users_realiazcia._Description
	when users_otvet_hranenie._Description is not null then users_otvet_hranenie._Description
	when users_peredacha_hranitel._Description is not null then users_peredacha_hranitel._Description
	else null
end
order by PN, iif(hoz_operacii.Синоним = 'Передача в состав основных средств',2,iif(hoz_operacii.Синоним='Сторно списания на расходы',1,iif(hoz_operacii.Синоним='Импорт',999,0))), cast(dateadd(year,-2000,registr_sebes._Period) as date) asc
        '''
	
	def get_elt_bn_kupol():
		return f'''
		select 
PN, ELT_BN
FROM (
select 'dba_virt_ARH_store' as StoreName, virt_ARH_store.* from [DBA].virt_ARH_store
union all
select 'dba_virt_KJA_store' as StoreName, virt_KJA_store.* from [DBA].virt_KJA_store
union all
select 'dba_VIRT_SVO_store' as StoreName, VIRT_SVO_store.* from [DBA].VIRT_SVO_store
union all
select 'dba_virt_SPB_store' as StoreName, virt_SPB_store.* from [DBA].virt_SPB_store
union all
select 'dba_VIRT_DME_store' as StoreName, VIRT_DME_store.* from [DBA].VIRT_DME_store
union all
select 'dba_VIRT_SCW_store' as StoreName, VIRT_SCW_store.* from [DBA].VIRT_SCW_store
union all
select 'dba_virt_s7_store' as StoreName, VIRT_S7_STORE.* from [DBA].VIRT_S7_STORE
union all
select 'dba_virt_AER_store' as StoreName, virt_AER_store.* from [DBA].virt_AER_store
union all
select 'dba_VIRT_KGD_store' as StoreName, VIRT_KGD_Store.* from [DBA].VIRT_KGD_Store
) elt_bn_stores
group by PN, ELT_BN
		'''
	

	def get_pn_kupol():
		return f'''
		select
cast(pn.pn as nvarchar) as pn,
pn1c.GUID1C
from [DBA].PN1CGUID pn1c
left join [DBA].PN pn on pn.id = pn1c.IDPN
where pn1c.ERPName != 'SAPNS'
		'''
	

	def get_isrs_from_kupol():
		return f'''
		select
cast(isr.ISRDate as date) as ISRDate,
cast(isr.ID as nvarchar) as IDISR, 
storefrom.StoreName as StoreFrom,
storeto.StoreName as StoreTo,
cast(isrs.ELT_BN as nvarchar) as ELT_BN,
cast(isrs.ELT_ID as nvarchar) as ELT_ID,
sum(isrs.QTY_Released) as QTY_Released,
isrs.PN as PN_Kupol,
isrs.SN,
sbt.BalanceCode,
isrs.IDProperty,
errors.KUPoLErrorText,
errors.KSIPResponse,
errors.MessageText,
pns.GUID1C,
pns.KeyWordTranslation,
pns.Description,
case 
	when isrs.IDProperty = '2873' then 'Собственник LMS'
	when isrs.IDProperty != '560' then 'Собственник не НордСтар'
	when storefrom.StoreName = 'VIRT_DME' and storeto.StoreName = 'SV_DME_NS2' then 'Перемещение между одинаковыми складами'
	when storefrom.StoreName = 'VIRT_KJA' and storeto.StoreName = 'SV_KJA_NS' then 'Перемещение между одинаковыми складами'
	when storefrom.StoreName = storeto.StoreName then 'Перемещение между одинаковыми складами'
	when storefrom.StoreName like '%_DME_UTG' and storeto.StoreName like '%_DME_NS2' then 'Перемещение между одинаковыми складами'
	when storefrom.StoreName like '%_DME_NS2' and storeto.StoreName like '%_DME_UTG' then 'Перемещение между одинаковыми складами'
    when LENGTH(TRIM(isrs.ELT_ID))>0 then 'Инструмент'
	when isrs.IDBalanceType is null then 'Нет кода баланса'
	else 'К отправке'
end as StatusISR,
case 
	when errors.KSIPResponse is null then 'Ошибка отправки'
	when errors.KSIPResponse = '-200' then 'Ограничения отправки на стороне КУПОЛ'
	when errors.KSIPResponse = '200' then 'Отправлено из КУПОЛ'
	else null
end as StatusLog,
case 
	when storefrom.StoreName = 'QR_DME_NS2' and sbt.BalanceCode = 'C' then 'ДТО. ДомодедовоК'
	--when storefrom.StoreName = 'QR_DME_NS2' and (sbt.BalanceCode = 'O' or sbt.BalanceCode = 'A') then 'ДТО. ДомодедовоК'
	when storefrom.StoreName = 'QR_KJA_NS' and sbt.BalanceCode = 'C' then 'ДТО. Красноярск К'
	when storefrom.StoreName = 'QR_ZIA_NS' and sbt.BalanceCode = 'C' then 'ТД ЖКВ К'
	when storefrom.StoreName = 'SV_ABA_NS' and sbt.BalanceCode = 'C' then 'ДТО. Абакан'
	when storefrom.StoreName = 'SV_ABROAD_CHECK_NS' and sbt.BalanceCode is not null then 'Алиев Р.Р. (No import)'
	when storefrom.StoreName = 'SV_DME_KRLOG' and sbt.BalanceCode is not null then 'ДТО. Абакан'
	when storefrom.StoreName = 'SV_DME_NS2' and sbt.BalanceCode = 'C' then 'ДТО. Домодедово'
	when storefrom.StoreName = 'SV_DME_NS2' and (sbt.BalanceCode = 'O' or sbt.BalanceCode = 'A') then 'ДТО. Домодедово (забаланс)'
	when storefrom.StoreName = 'SV_DME_UTG' and sbt.BalanceCode = 'C' then 'ДТО. Домодедово'
	when storefrom.StoreName = 'SV_DME_UTG' and (sbt.BalanceCode = 'O' or sbt.BalanceCode = 'A') then 'ДТО. Домодедово (забаланс)'
	when storefrom.StoreName = 'SV_KJA' and sbt.BalanceCode = 'C' then 'ДТО. Красноярск'
	when storefrom.StoreName = 'SV_KJA' and (sbt.BalanceCode = 'O' or sbt.BalanceCode = 'A') then 'ДТО. Красноярск (забаланс)'
	when storefrom.StoreName = 'SV_KJA_NS' and sbt.BalanceCode = 'C' then 'ДТО. Красноярск'
	when storefrom.StoreName = 'SV_KJA_NS' and (sbt.BalanceCode = 'O' or sbt.BalanceCode = 'A') then 'ДТО. Красноярск (забаланс)'
	when storefrom.StoreName = 'SV_NSK_NS2' and sbt.BalanceCode = 'C' then 'ДТО. Норильск'
	when storefrom.StoreName = 'SV_NSK_NS2' and (sbt.BalanceCode = 'O' or sbt.BalanceCode = 'A') then 'ДТО. Норильск (забаланс)'
	when storefrom.StoreName = 'SV_SVO_NS' and sbt.BalanceCode = 'C' then 'ДТО. Домодедово'
	when storefrom.StoreName = 'SV_SVO_NS' and (sbt.BalanceCode = 'O' or sbt.BalanceCode = 'A') then 'ДТО. Домодедово (забаланс)'
	when storefrom.StoreName = 'SV_VKO_UTG_NS' and sbt.BalanceCode = 'C' then 'ДТО. Домодедово'
	when storefrom.StoreName = 'SV_VKO_UTG_NS' and (sbt.BalanceCode = 'O' or sbt.BalanceCode = 'A') then 'ДТО. Домодедово (забаланс)'
	when storefrom.StoreName = 'SV_ZIA_NS' and sbt.BalanceCode = 'C' then 'ТД ЖКВ'
	when storefrom.StoreName = 'SV_ZIA_NS' and (sbt.BalanceCode = 'O' or sbt.BalanceCode = 'A') then 'ТД ЖКВ БУ'
	when storefrom.StoreName = 'SV_ZIA_UTG_NS' and sbt.BalanceCode = 'C' then 'ТД ЖКВ'
	when storefrom.StoreName = 'SV_ZIA_UTG_NS' and (sbt.BalanceCode = 'O' or sbt.BalanceCode = 'A') then 'ТД ЖКВ БУ'
	when storefrom.StoreName = 'US_DME_NS2' and sbt.BalanceCode = 'C' then 'ДТО. Домодедово б/у'
	when storefrom.StoreName = 'US_DME_NS2' and (sbt.BalanceCode = 'O' or sbt.BalanceCode = 'A') then 'ДТО. Домодедово б/у (забаланс)'
	when storefrom.StoreName = 'US_DME_UTG' and sbt.BalanceCode = 'C' then 'ДТО. Домодедово б/у'
	when storefrom.StoreName = 'US_DME_UTG' and (sbt.BalanceCode = 'O' or sbt.BalanceCode = 'A') then 'ДТО. Домодедово б/у (забаланс)'
	when storefrom.StoreName = 'US_KJA_NS' and sbt.BalanceCode = 'C' then 'ДТО. Красноярск б/у'
	when storefrom.StoreName = 'US_KJA_NS' and (sbt.BalanceCode = 'O' or sbt.BalanceCode = 'A') then 'ДТО. Красноярск б/у (забаланс)'
	when storefrom.StoreName = 'US_NSK_NS2' and sbt.BalanceCode = 'C' then 'ДТО. Норильск б/у'
	when storefrom.StoreName = 'US_NSK_NS2' and (sbt.BalanceCode = 'O' or sbt.BalanceCode = 'A') then 'ДТО. Норильск б/у (забаланс)'
	when storefrom.StoreName = 'US_SVO_NS' and sbt.BalanceCode = 'C' then 'ДТО. Домодедово б/у'
	when storefrom.StoreName = 'US_SVO_NS' and (sbt.BalanceCode = 'O' or sbt.BalanceCode = 'A') then 'ДТО. Домодедово б/у (забаланс)'
	when storefrom.StoreName = 'US_ZIA_NS' and sbt.BalanceCode = 'C' then 'ТД ЖКВ_З'
	when storefrom.StoreName = 'US_ZIA_NS' and (sbt.BalanceCode = 'O' or sbt.BalanceCode = 'A') then 'ТД ЖКВ_З БУ'
	when storefrom.StoreName = 'US_ZIA_UTG_NS' and sbt.BalanceCode = 'C' then 'ТД ЖКВ БУ'
	when storefrom.StoreName = 'US_ZIA_UTG_NS' and (sbt.BalanceCode = 'O' or sbt.BalanceCode = 'A') then 'ТД ЖКВ_З БУ'
	when storefrom.StoreName = 'VIRT_DME' and sbt.BalanceCode = 'C' then 'ДТО. Домодедово'
	when storefrom.StoreName = 'VIRT_DME' and (sbt.BalanceCode = 'O' or sbt.BalanceCode = 'A') then 'ДТО. Домодедово (забаланс)'
	when storefrom.StoreName = 'VIRT_DME' and sbt.BalanceCode = 'C' then 'ДТО. Красноярск'
	when storefrom.StoreName = 'VIRT_DME' and (sbt.BalanceCode = 'O' or sbt.BalanceCode = 'A') then 'ДТО. Красноярск (забаланс)'
	when storefrom.StoreName = 'VIRT_SVO' and sbt.BalanceCode = 'C' then 'ДТО. Домодедово'
	when storefrom.StoreName = 'VIRT_SVO' and (sbt.BalanceCode = 'O' or sbt.BalanceCode = 'A') then 'ДТО. Домодедово (забаланс)'
end as storefrom_1c,
case 
	when storeto.StoreName = 'QR_DME_NS2' and sbt.BalanceCode = 'C' then 'ДТО. ДомодедовоК'
	--when storeto.StoreName = 'QR_DME_NS2' and (sbt.BalanceCode = 'O' or sbt.BalanceCode = 'A') then 'ДТО. ДомодедовоК'
	when storeto.StoreName = 'QR_KJA_NS' and sbt.BalanceCode = 'C' then 'ДТО. Красноярск К'
	when storeto.StoreName = 'QR_ZIA_NS' and sbt.BalanceCode = 'C' then 'ТД ЖКВ К'
	when storeto.StoreName = 'SV_ABA_NS' and sbt.BalanceCode = 'C' then 'ДТО. Абакан'
	when storeto.StoreName = 'SV_ABROAD_CHECK_NS' and sbt.BalanceCode is not null then 'Алиев Р.Р. (No import)'
	when storeto.StoreName = 'SV_DME_KRLOG' and sbt.BalanceCode is not null then 'ДТО. Абакан'
	when storeto.StoreName = 'SV_DME_NS2' and sbt.BalanceCode = 'C' then 'ДТО. Домодедово'
	when storeto.StoreName = 'SV_DME_NS2' and (sbt.BalanceCode = 'O' or sbt.BalanceCode = 'A') then 'ДТО. Домодедово (забаланс)'
	when storeto.StoreName = 'SV_DME_UTG' and sbt.BalanceCode = 'C' then 'ДТО. Домодедово'
	when storeto.StoreName = 'SV_DME_UTG' and (sbt.BalanceCode = 'O' or sbt.BalanceCode = 'A') then 'ДТО. Домодедово (забаланс)'
	when storeto.StoreName = 'SV_KJA' and sbt.BalanceCode = 'C' then 'ДТО. Красноярск'
	when storeto.StoreName = 'SV_KJA' and (sbt.BalanceCode = 'O' or sbt.BalanceCode = 'A') then 'ДТО. Красноярск (забаланс)'
	when storeto.StoreName = 'SV_KJA_NS' and sbt.BalanceCode = 'C' then 'ДТО. Красноярск'
	when storeto.StoreName = 'SV_KJA_NS' and (sbt.BalanceCode = 'O' or sbt.BalanceCode = 'A') then 'ДТО. Красноярск (забаланс)'
	when storeto.StoreName = 'SV_NSK_NS2' and sbt.BalanceCode = 'C' then 'ДТО. Норильск'
	when storeto.StoreName = 'SV_NSK_NS2' and (sbt.BalanceCode = 'O' or sbt.BalanceCode = 'A') then 'ДТО. Норильск (забаланс)'
	when storeto.StoreName = 'SV_SVO_NS' and sbt.BalanceCode = 'C' then 'ДТО. Домодедово'
	when storeto.StoreName = 'SV_SVO_NS' and (sbt.BalanceCode = 'O' or sbt.BalanceCode = 'A') then 'ДТО. Домодедово (забаланс)'
	when storeto.StoreName = 'SV_VKO_UTG_NS' and sbt.BalanceCode = 'C' then 'ДТО. Домодедово'
	when storeto.StoreName = 'SV_VKO_UTG_NS' and (sbt.BalanceCode = 'O' or sbt.BalanceCode = 'A') then 'ДТО. Домодедово (забаланс)'
	when storeto.StoreName = 'SV_ZIA_NS' and sbt.BalanceCode = 'C' then 'ТД ЖКВ'
	when storeto.StoreName = 'SV_ZIA_NS' and (sbt.BalanceCode = 'O' or sbt.BalanceCode = 'A') then 'ТД ЖКВ БУ'
	when storeto.StoreName = 'SV_ZIA_UTG_NS' and sbt.BalanceCode = 'C' then 'ТД ЖКВ'
	when storeto.StoreName = 'SV_ZIA_UTG_NS' and (sbt.BalanceCode = 'O' or sbt.BalanceCode = 'A') then 'ТД ЖКВ БУ'
	when storeto.StoreName = 'US_DME_NS2' and sbt.BalanceCode = 'C' then 'ДТО. Домодедово б/у'
	when storeto.StoreName = 'US_DME_NS2' and (sbt.BalanceCode = 'O' or sbt.BalanceCode = 'A') then 'ДТО. Домодедово б/у (забаланс)'
	when storeto.StoreName = 'US_DME_UTG' and sbt.BalanceCode = 'C' then 'ДТО. Домодедово б/у'
	when storeto.StoreName = 'US_DME_UTG' and (sbt.BalanceCode = 'O' or sbt.BalanceCode = 'A') then 'ДТО. Домодедово б/у (забаланс)'
	when storeto.StoreName = 'US_KJA_NS' and sbt.BalanceCode = 'C' then 'ДТО. Красноярск б/у'
	when storeto.StoreName = 'US_KJA_NS' and (sbt.BalanceCode = 'O' or sbt.BalanceCode = 'A') then 'ДТО. Красноярск б/у (забаланс)'
	when storeto.StoreName = 'US_NSK_NS2' and sbt.BalanceCode = 'C' then 'ДТО. Норильск б/у'
	when storeto.StoreName = 'US_NSK_NS2' and (sbt.BalanceCode = 'O' or sbt.BalanceCode = 'A') then 'ДТО. Норильск б/у (забаланс)'
	when storeto.StoreName = 'US_SVO_NS' and sbt.BalanceCode = 'C' then 'ДТО. Домодедово б/у'
	when storeto.StoreName = 'US_SVO_NS' and (sbt.BalanceCode = 'O' or sbt.BalanceCode = 'A') then 'ДТО. Домодедово б/у (забаланс)'
	when storeto.StoreName = 'US_ZIA_NS' and sbt.BalanceCode = 'C' then 'ТД ЖКВ_З'
	when storeto.StoreName = 'US_ZIA_NS' and (sbt.BalanceCode = 'O' or sbt.BalanceCode = 'A') then 'ТД ЖКВ_З БУ'
	when storeto.StoreName = 'US_ZIA_UTG_NS' and sbt.BalanceCode = 'C' then 'ТД ЖКВ БУ'
	when storeto.StoreName = 'US_ZIA_UTG_NS' and (sbt.BalanceCode = 'O' or sbt.BalanceCode = 'A') then 'ТД ЖКВ_З БУ'
	when storeto.StoreName = 'VIRT_DME' and sbt.BalanceCode = 'C' then 'ДТО. Домодедово'
	when storeto.StoreName = 'VIRT_DME' and (sbt.BalanceCode = 'O' or sbt.BalanceCode = 'A') then 'ДТО. Домодедово (забаланс)'
	when storeto.StoreName = 'VIRT_DME' and sbt.BalanceCode = 'C' then 'ДТО. Красноярск'
	when storeto.StoreName = 'VIRT_DME' and (sbt.BalanceCode = 'O' or sbt.BalanceCode = 'A') then 'ДТО. Красноярск (забаланс)'
	when storeto.StoreName = 'VIRT_SVO' and sbt.BalanceCode = 'C' then 'ДТО. Домодедово'
	when storeto.StoreName = 'VIRT_SVO' and (sbt.BalanceCode = 'O' or sbt.BalanceCode = 'A') then 'ДТО. Домодедово (забаланс)'
end as storeto_1c
from [DBA].InterStoreRelocation isr
left join [DBA].StoreList storefrom on storefrom.ID = isr.IDFromStore
left join [DBA].StoreList storeto on storeto.ID = isr.IDToStore
left join [DBA].ISRItems isrs on isrs.IDISR = isr.ID 
left join (
SELECT IDCustomer, IDOperationType, IDMessage, IDStore, MessageOrder, max(MessageTime) as MessageTime, KSIPResponse, MessageText, KUPoLErrorText
FROM [DBA].ISAPMessageOrder
join (select max(imo.ID) as MssgTime, imo.IDMessage as IDMssg, imo.IDCustomer as IDCustomers from [DBA].ISAPMessageOrder imo GROUP BY IDMessage, IDCustomer) io 
on io.MssgTime = [DBA].ISAPMessageOrder.ID and io.IDMssg = [DBA].ISAPMessageOrder.IDMessage and io.IDCustomers = [DBA].ISAPMessageOrder.IDCustomer
WHERE IDOperationType = 2 and (KUPoLErrorText is not null or MessageText is not null)
GROUP BY IDCustomer, IDOperationType, IDMessage, IDStore, MessageOrder, KSIPResponse, KUPoLErrorText, MessageText
order by MessageTime desc
) errors on errors.IDMessage = isr.ID and errors.IDCustomer = isrs.IDProperty
left join (
select p.PN as PN, CONVERT(nvarchar, p.KeyWordTranslation) as KeyWordTranslation, mc.Description, mc.Code, p1c.GUID1C
from DBA.PN p 
left join [DBA].PN1CGUID p1c on p.ID = p1c.IDPN and p1c.ERPName = '1CNS'
left join mma.MaterialClass mc on mc.ID = p.IDMCl
) pns on pns.PN = isrs.PN
left join [dba].StoreBalanceType sbt on sbt.id = isrs.IDBalanceType
where cast(isr.ISRDate as date) >= '2023-03-14'
group by 
cast(isr.ISRDate as date),
isr.ID, 
storefrom.StoreName,
storeto.StoreName,
cast(isrs.ELT_BN as nvarchar),
cast(isrs.ELT_ID as nvarchar),
isrs.PN,
isrs.SN,
sbt.BalanceCode,
isrs.IDProperty,
errors.KUPoLErrorText,
errors.KSIPResponse,
errors.MessageText,
pns.GUID1C,
pns.KeyWordTranslation,
pns.Description,
case 
	when isrs.IDProperty = '2873' then 'Собственник LMS'
	when isrs.IDProperty != '560' then 'Собственник не НордСтар'
	when storefrom.StoreName = 'VIRT_DME' and storeto.StoreName = 'SV_DME_NS2' then 'Перемещение между одинаковыми складами'
	when storefrom.StoreName = 'VIRT_KJA' and storeto.StoreName = 'SV_KJA_NS' then 'Перемещение между одинаковыми складами'
	when storefrom.StoreName = storeto.StoreName then 'Перемещение между одинаковыми складами'
	when storefrom.StoreName like '%_DME_UTG' and storeto.StoreName like '%_DME_NS2' then 'Перемещение между одинаковыми складами'
	when storefrom.StoreName like '%_DME_NS2' and storeto.StoreName like '%_DME_UTG' then 'Перемещение между одинаковыми складами'
    when LENGTH(TRIM(isrs.ELT_ID))>0 then 'Инструмент'
	when isrs.IDBalanceType is null then 'Нет кода баланса'
	else 'К отправке'
end,
case 
	when errors.KSIPResponse is null then 'Ошибка отправки'
	when errors.KSIPResponse = '-200' then 'Ограничения отправки на стороне КУПОЛ'
	when errors.KSIPResponse = '200' then 'Отправлено из КУПОЛ'
	else null
end,
case 
	when storefrom.StoreName = 'QR_DME_NS2' and sbt.BalanceCode = 'C' then 'ДТО. ДомодедовоК'
	--when storefrom.StoreName = 'QR_DME_NS2' and (sbt.BalanceCode = 'O' or sbt.BalanceCode = 'A') then 'ДТО. ДомодедовоК'
	when storefrom.StoreName = 'QR_KJA_NS' and sbt.BalanceCode = 'C' then 'ДТО. Красноярск К'
	when storefrom.StoreName = 'QR_ZIA_NS' and sbt.BalanceCode = 'C' then 'ТД ЖКВ К'
	when storefrom.StoreName = 'SV_ABA_NS' and sbt.BalanceCode = 'C' then 'ДТО. Абакан'
	when storefrom.StoreName = 'SV_ABROAD_CHECK_NS' and sbt.BalanceCode is not null then 'Алиев Р.Р. (No import)'
	when storefrom.StoreName = 'SV_DME_KRLOG' and sbt.BalanceCode is not null then 'ДТО. Абакан'
	when storefrom.StoreName = 'SV_DME_NS2' and sbt.BalanceCode = 'C' then 'ДТО. Домодедово'
	when storefrom.StoreName = 'SV_DME_NS2' and (sbt.BalanceCode = 'O' or sbt.BalanceCode = 'A') then 'ДТО. Домодедово (забаланс)'
	when storefrom.StoreName = 'SV_DME_UTG' and sbt.BalanceCode = 'C' then 'ДТО. Домодедово'
	when storefrom.StoreName = 'SV_DME_UTG' and (sbt.BalanceCode = 'O' or sbt.BalanceCode = 'A') then 'ДТО. Домодедово (забаланс)'
	when storefrom.StoreName = 'SV_KJA' and sbt.BalanceCode = 'C' then 'ДТО. Красноярск'
	when storefrom.StoreName = 'SV_KJA' and (sbt.BalanceCode = 'O' or sbt.BalanceCode = 'A') then 'ДТО. Красноярск (забаланс)'
	when storefrom.StoreName = 'SV_KJA_NS' and sbt.BalanceCode = 'C' then 'ДТО. Красноярск'
	when storefrom.StoreName = 'SV_KJA_NS' and (sbt.BalanceCode = 'O' or sbt.BalanceCode = 'A') then 'ДТО. Красноярск (забаланс)'
	when storefrom.StoreName = 'SV_NSK_NS2' and sbt.BalanceCode = 'C' then 'ДТО. Норильск'
	when storefrom.StoreName = 'SV_NSK_NS2' and (sbt.BalanceCode = 'O' or sbt.BalanceCode = 'A') then 'ДТО. Норильск (забаланс)'
	when storefrom.StoreName = 'SV_SVO_NS' and sbt.BalanceCode = 'C' then 'ДТО. Домодедово'
	when storefrom.StoreName = 'SV_SVO_NS' and (sbt.BalanceCode = 'O' or sbt.BalanceCode = 'A') then 'ДТО. Домодедово (забаланс)'
	when storefrom.StoreName = 'SV_VKO_UTG_NS' and sbt.BalanceCode = 'C' then 'ДТО. Домодедово'
	when storefrom.StoreName = 'SV_VKO_UTG_NS' and (sbt.BalanceCode = 'O' or sbt.BalanceCode = 'A') then 'ДТО. Домодедово (забаланс)'
	when storefrom.StoreName = 'SV_ZIA_NS' and sbt.BalanceCode = 'C' then 'ТД ЖКВ'
	when storefrom.StoreName = 'SV_ZIA_NS' and (sbt.BalanceCode = 'O' or sbt.BalanceCode = 'A') then 'ТД ЖКВ БУ'
	when storefrom.StoreName = 'SV_ZIA_UTG_NS' and sbt.BalanceCode = 'C' then 'ТД ЖКВ'
	when storefrom.StoreName = 'SV_ZIA_UTG_NS' and (sbt.BalanceCode = 'O' or sbt.BalanceCode = 'A') then 'ТД ЖКВ БУ'
	when storefrom.StoreName = 'US_DME_NS2' and sbt.BalanceCode = 'C' then 'ДТО. Домодедово б/у'
	when storefrom.StoreName = 'US_DME_NS2' and (sbt.BalanceCode = 'O' or sbt.BalanceCode = 'A') then 'ДТО. Домодедово б/у (забаланс)'
	when storefrom.StoreName = 'US_DME_UTG' and sbt.BalanceCode = 'C' then 'ДТО. Домодедово б/у'
	when storefrom.StoreName = 'US_DME_UTG' and (sbt.BalanceCode = 'O' or sbt.BalanceCode = 'A') then 'ДТО. Домодедово б/у (забаланс)'
	when storefrom.StoreName = 'US_KJA_NS' and sbt.BalanceCode = 'C' then 'ДТО. Красноярск б/у'
	when storefrom.StoreName = 'US_KJA_NS' and (sbt.BalanceCode = 'O' or sbt.BalanceCode = 'A') then 'ДТО. Красноярск б/у (забаланс)'
	when storefrom.StoreName = 'US_NSK_NS2' and sbt.BalanceCode = 'C' then 'ДТО. Норильск б/у'
	when storefrom.StoreName = 'US_NSK_NS2' and (sbt.BalanceCode = 'O' or sbt.BalanceCode = 'A') then 'ДТО. Норильск б/у (забаланс)'
	when storefrom.StoreName = 'US_SVO_NS' and sbt.BalanceCode = 'C' then 'ДТО. Домодедово б/у'
	when storefrom.StoreName = 'US_SVO_NS' and (sbt.BalanceCode = 'O' or sbt.BalanceCode = 'A') then 'ДТО. Домодедово б/у (забаланс)'
	when storefrom.StoreName = 'US_ZIA_NS' and sbt.BalanceCode = 'C' then 'ТД ЖКВ_З'
	when storefrom.StoreName = 'US_ZIA_NS' and (sbt.BalanceCode = 'O' or sbt.BalanceCode = 'A') then 'ТД ЖКВ_З БУ'
	when storefrom.StoreName = 'US_ZIA_UTG_NS' and sbt.BalanceCode = 'C' then 'ТД ЖКВ БУ'
	when storefrom.StoreName = 'US_ZIA_UTG_NS' and (sbt.BalanceCode = 'O' or sbt.BalanceCode = 'A') then 'ТД ЖКВ_З БУ'
	when storefrom.StoreName = 'VIRT_DME' and sbt.BalanceCode = 'C' then 'ДТО. Домодедово'
	when storefrom.StoreName = 'VIRT_DME' and (sbt.BalanceCode = 'O' or sbt.BalanceCode = 'A') then 'ДТО. Домодедово (забаланс)'
	when storefrom.StoreName = 'VIRT_DME' and sbt.BalanceCode = 'C' then 'ДТО. Красноярск'
	when storefrom.StoreName = 'VIRT_DME' and (sbt.BalanceCode = 'O' or sbt.BalanceCode = 'A') then 'ДТО. Красноярск (забаланс)'
	when storefrom.StoreName = 'VIRT_SVO' and sbt.BalanceCode = 'C' then 'ДТО. Домодедово'
	when storefrom.StoreName = 'VIRT_SVO' and (sbt.BalanceCode = 'O' or sbt.BalanceCode = 'A') then 'ДТО. Домодедово (забаланс)'
end,
case 
	when storeto.StoreName = 'QR_DME_NS2' and sbt.BalanceCode = 'C' then 'ДТО. ДомодедовоК'
	--when storeto.StoreName = 'QR_DME_NS2' and (sbt.BalanceCode = 'O' or sbt.BalanceCode = 'A') then 'ДТО. ДомодедовоК'
	when storeto.StoreName = 'QR_KJA_NS' and sbt.BalanceCode = 'C' then 'ДТО. Красноярск К'
	when storeto.StoreName = 'QR_ZIA_NS' and sbt.BalanceCode = 'C' then 'ТД ЖКВ К'
	when storeto.StoreName = 'SV_ABA_NS' and sbt.BalanceCode = 'C' then 'ДТО. Абакан'
	when storeto.StoreName = 'SV_ABROAD_CHECK_NS' and sbt.BalanceCode is not null then 'Алиев Р.Р. (No import)'
	when storeto.StoreName = 'SV_DME_KRLOG' and sbt.BalanceCode is not null then 'ДТО. Абакан'
	when storeto.StoreName = 'SV_DME_NS2' and sbt.BalanceCode = 'C' then 'ДТО. Домодедово'
	when storeto.StoreName = 'SV_DME_NS2' and (sbt.BalanceCode = 'O' or sbt.BalanceCode = 'A') then 'ДТО. Домодедово (забаланс)'
	when storeto.StoreName = 'SV_DME_UTG' and sbt.BalanceCode = 'C' then 'ДТО. Домодедово'
	when storeto.StoreName = 'SV_DME_UTG' and (sbt.BalanceCode = 'O' or sbt.BalanceCode = 'A') then 'ДТО. Домодедово (забаланс)'
	when storeto.StoreName = 'SV_KJA' and sbt.BalanceCode = 'C' then 'ДТО. Красноярск'
	when storeto.StoreName = 'SV_KJA' and (sbt.BalanceCode = 'O' or sbt.BalanceCode = 'A') then 'ДТО. Красноярск (забаланс)'
	when storeto.StoreName = 'SV_KJA_NS' and sbt.BalanceCode = 'C' then 'ДТО. Красноярск'
	when storeto.StoreName = 'SV_KJA_NS' and (sbt.BalanceCode = 'O' or sbt.BalanceCode = 'A') then 'ДТО. Красноярск (забаланс)'
	when storeto.StoreName = 'SV_NSK_NS2' and sbt.BalanceCode = 'C' then 'ДТО. Норильск'
	when storeto.StoreName = 'SV_NSK_NS2' and (sbt.BalanceCode = 'O' or sbt.BalanceCode = 'A') then 'ДТО. Норильск (забаланс)'
	when storeto.StoreName = 'SV_SVO_NS' and sbt.BalanceCode = 'C' then 'ДТО. Домодедово'
	when storeto.StoreName = 'SV_SVO_NS' and (sbt.BalanceCode = 'O' or sbt.BalanceCode = 'A') then 'ДТО. Домодедово (забаланс)'
	when storeto.StoreName = 'SV_VKO_UTG_NS' and sbt.BalanceCode = 'C' then 'ДТО. Домодедово'
	when storeto.StoreName = 'SV_VKO_UTG_NS' and (sbt.BalanceCode = 'O' or sbt.BalanceCode = 'A') then 'ДТО. Домодедово (забаланс)'
	when storeto.StoreName = 'SV_ZIA_NS' and sbt.BalanceCode = 'C' then 'ТД ЖКВ'
	when storeto.StoreName = 'SV_ZIA_NS' and (sbt.BalanceCode = 'O' or sbt.BalanceCode = 'A') then 'ТД ЖКВ БУ'
	when storeto.StoreName = 'SV_ZIA_UTG_NS' and sbt.BalanceCode = 'C' then 'ТД ЖКВ'
	when storeto.StoreName = 'SV_ZIA_UTG_NS' and (sbt.BalanceCode = 'O' or sbt.BalanceCode = 'A') then 'ТД ЖКВ БУ'
	when storeto.StoreName = 'US_DME_NS2' and sbt.BalanceCode = 'C' then 'ДТО. Домодедово б/у'
	when storeto.StoreName = 'US_DME_NS2' and (sbt.BalanceCode = 'O' or sbt.BalanceCode = 'A') then 'ДТО. Домодедово б/у (забаланс)'
	when storeto.StoreName = 'US_DME_UTG' and sbt.BalanceCode = 'C' then 'ДТО. Домодедово б/у'
	when storeto.StoreName = 'US_DME_UTG' and (sbt.BalanceCode = 'O' or sbt.BalanceCode = 'A') then 'ДТО. Домодедово б/у (забаланс)'
	when storeto.StoreName = 'US_KJA_NS' and sbt.BalanceCode = 'C' then 'ДТО. Красноярск б/у'
	when storeto.StoreName = 'US_KJA_NS' and (sbt.BalanceCode = 'O' or sbt.BalanceCode = 'A') then 'ДТО. Красноярск б/у (забаланс)'
	when storeto.StoreName = 'US_NSK_NS2' and sbt.BalanceCode = 'C' then 'ДТО. Норильск б/у'
	when storeto.StoreName = 'US_NSK_NS2' and (sbt.BalanceCode = 'O' or sbt.BalanceCode = 'A') then 'ДТО. Норильск б/у (забаланс)'
	when storeto.StoreName = 'US_SVO_NS' and sbt.BalanceCode = 'C' then 'ДТО. Домодедово б/у'
	when storeto.StoreName = 'US_SVO_NS' and (sbt.BalanceCode = 'O' or sbt.BalanceCode = 'A') then 'ДТО. Домодедово б/у (забаланс)'
	when storeto.StoreName = 'US_ZIA_NS' and sbt.BalanceCode = 'C' then 'ТД ЖКВ_З'
	when storeto.StoreName = 'US_ZIA_NS' and (sbt.BalanceCode = 'O' or sbt.BalanceCode = 'A') then 'ТД ЖКВ_З БУ'
	when storeto.StoreName = 'US_ZIA_UTG_NS' and sbt.BalanceCode = 'C' then 'ТД ЖКВ БУ'
	when storeto.StoreName = 'US_ZIA_UTG_NS' and (sbt.BalanceCode = 'O' or sbt.BalanceCode = 'A') then 'ТД ЖКВ_З БУ'
	when storeto.StoreName = 'VIRT_DME' and sbt.BalanceCode = 'C' then 'ДТО. Домодедово'
	when storeto.StoreName = 'VIRT_DME' and (sbt.BalanceCode = 'O' or sbt.BalanceCode = 'A') then 'ДТО. Домодедово (забаланс)'
	when storeto.StoreName = 'VIRT_DME' and sbt.BalanceCode = 'C' then 'ДТО. Красноярск'
	when storeto.StoreName = 'VIRT_DME' and (sbt.BalanceCode = 'O' or sbt.BalanceCode = 'A') then 'ДТО. Красноярск (забаланс)'
	when storeto.StoreName = 'VIRT_SVO' and sbt.BalanceCode = 'C' then 'ДТО. Домодедово'
	when storeto.StoreName = 'VIRT_SVO' and (sbt.BalanceCode = 'O' or sbt.BalanceCode = 'A') then 'ДТО. Домодедово (забаланс)'
end
		'''
	

	def get_isrs_from_1c():
		return f'''
		select
case 
	when ptu_registr._Number is not null then 'Приобретение товаров и услуг ' + ptu_registr._Number
	when spis_registr._Number is not null then 'Списание на расходы ' + spis_registr._Number
 	when vozvrat_tovarov._Number is not null then 'Возврат товаров поставщику ' + vozvrat_tovarov._Number
	when peremestit._Number is not null then 'Перемещение товаров ' + peremestit._Number
	when storno_spis._Number is not null then 'Сторно списания на расходы ' + storno_spis._Number
	when peredacha._Number is not null then 'Передача переработчику ' + peredacha._Number
	when vozvrat_siria._Number is not null then 'Возврат от переработчика ' + vozvrat_siria._Number
	when sborka_razborka._Number is not null then 'Сборка (разборка) товаров ' + sborka_razborka._Number
	when realiazcia._Number is not null then 'Реализация товаров и услуг ' + realiazcia._Number
	when otvet_hranenie._Number is not null then 'Приемка товаров на хранение' + otvet_hranenie._Number
	when peredacha_hranitel._Number is not null then 'Передача на ответ хранение' + peredacha_hranitel._Number
	else registr_sebes._RecorderRRef
end as Registrator,
case	
	when ptu_registr._Number is not null then 'Приобретение товаров и услуг'
	when spis_registr._Number is not null then 'Списание на расходы'
 	when vozvrat_tovarov._Number is not null then 'Возврат товаров поставщику'
	when peremestit._Number is not null then 'Перемещение товаров'
	when storno_spis._Number is not null then 'Сторно списания на расходы'
	when peredacha._Number is not null then 'Передача переработчику'
	when vozvrat_siria._Number is not null then 'Возврат от переработчика'
	when sborka_razborka._Number is not null then 'Сборка (разборка) товаров'
	when realiazcia._Number is not null then 'Реализация товаров и услуг'
	when otvet_hranenie._Number is not null then 'Приемка товаров на хранение' 
	when peredacha_hranitel._Number is not null then 'Передача на ответ хранение'
	else registr_sebes._RecorderRRef 
end as Registrator_name,
case 
	when ptu_registr._Number is not null then ptu_registr._Number
	when spis_registr._Number is not null then spis_registr._Number
 	when vozvrat_tovarov._Number is not null then  vozvrat_tovarov._Number
	when peremestit._Number is not null then peremestit._Number
	when storno_spis._Number is not null then storno_spis._Number
	when peredacha._Number is not null then peredacha._Number
	when vozvrat_siria._Number is not null then vozvrat_siria._Number
	when sborka_razborka._Number is not null then sborka_razborka._Number
	when realiazcia._Number is not null then realiazcia._Number
	when otvet_hranenie._Number is not null then otvet_hranenie._Number
	when peredacha_hranitel._Number is not null then peredacha_hranitel._Number
	else registr_sebes._RecorderRRef
end as Registrator_number,
gtds.gtd_number as gtd_number,
/*iif(ptu._Number is not null, ptu._Number, 
iif(otvet_hranenie_partia._Number is not null, otvet_hranenie_partia._Number,
registr_sebes._Fld92745_RRRef))  as Partia,*/
cast(dateadd(year,-2000,registr_sebes._Period) as date) as date_doc,
nomenklatura.Nomen_code as Nomen_code,
nomenklatura.Nomen_name as Name,
monitor.SO_Number as SO_Number,
case 
	when monitor.elt_bn_ is null then seria.[_Description]
	else monitor.elt_bn_
end as Seria,
--seria.[_Description] as Seria,
--monitor.elt_bn_ as elt_bn_,
nomenklatura.Nomen_pn as PN_1C,
sum(registr_sebes._Fld92749) as qty,
sum(iif(registr_sebes._RecordKind=1,registr_sebes._Fld92749*-1,registr_sebes._Fld92749)) as qty_kind,
sum(registr_sebes._Fld92760) as sum_,
sum(monitor.Qty_SO) as Qty_monitor,
case 
	when sum(monitor.Qty_SO) <= sum(registr_sebes._Fld92749) then sum(monitor.Qty_SO)/count(monitor.Qty_SO)
	else sum(registr_sebes._Fld92749)
end as Qty_itog_1C,
--monitor.Item_SO as Item_SO,
iif(registr_sebes._RecordKind=1,'Списание','Поступление') as Status,
hoz_operacii.Синоним as Hoz_op,
orders._Description as order_,
IIF(object_rashod._Description is not null, object_rashod._Description, 
IIF(partners_analitika._Description is not null, partners_analitika._Description,
IIF(nd_analitika._Description is not null, nd_analitika._Description, 
registr_sebes._Fld92784_RRRef)))  as Analitika_rashodov,
right(IIF(object_rashod._Description is not null, object_rashod._Description, 
IIF(partners_analitika._Description is not null, partners_analitika._Description,
IIF(nd_analitika._Description is not null, nd_analitika._Description, 
registr_sebes._Fld92784_RRRef))),8) as registration_number
--partners._Description as Partner,
/*case 
	when cast(dateadd(year,-2000,registr_sebes._Period) as date) <= '2023-03-13' then 'Дата документа меньше, чем 14.03'
	else null
end as statusregistr_1c_so,
case 
	when users_ptu._Description is not null then users_ptu._Description
	when users_spis_registr._Description is not null then users_spis_registr._Description
	when users_vozvrat_tovarov._Description is not null then users_vozvrat_tovarov._Description
	when users_peremestit._Description is not null then users_peremestit._Description
	when users_storno_spis._Description is not null then users_storno_spis._Description
	when users_peredacha._Description is not null then users_peredacha._Description
	when users_vozvrat_siria._Description is not null then users_vozvrat_siria._Description
	when users_sborka_razborka._Description is not null then users_sborka_razborka._Description
	when users_realiazcia._Description is not null then users_realiazcia._Description
	when users_otvet_hranenie._Description is not null then users_otvet_hranenie._Description
	when users_peredacha_hranitel._Description is not null then users_peredacha_hranitel._Description
	else null
end as users*/
from _AccumRg92740 registr_sebes
left join _Document1540 ptu on ptu._IDRRef = registr_sebes._Fld92745_RRRef
left join _Document1527 otvet_hranenie_partia on otvet_hranenie_partia._IDRRef = registr_sebes._Fld92745_RRRef
left join _Document1540 ptu_registr on ptu_registr._IDRRef = registr_sebes._RecorderRRef
left join _Document1178 spis_registr on spis_registr._IDRRef = registr_sebes._RecorderRRef
left join _Reference452 analitik_nomen on analitik_nomen._IDRRef = registr_sebes._Fld92741RRef
left join _Reference848 orders on orders._IDRRef = analitik_nomen._Fld53262_RRRef
left join _Reference558 object_rashod on object_rashod._IDRRef = registr_sebes._Fld92784_RRRef
left join _Reference453 analitik_partia on analitik_partia._IDRRef = registr_sebes._Fld92746RRef
left join _Reference640 partners on partners._IDRRef = analitik_partia._Fld53274RRef
left join _Document1191 vozvrat_tovarov on vozvrat_tovarov._IDRRef = registr_sebes._RecorderRRef
left join _Document1475 peremestit on peremestit._IDRRef = registr_sebes._RecorderRRef
left join _Document1553 storno_spis on storno_spis._IDRRef = registr_sebes._RecorderRRef
left join _Document1461 peredacha on peredacha._IDRRef = registr_sebes._RecorderRRef
left join _Document1188 vozvrat_siria on vozvrat_siria._IDRRef = registr_sebes._RecorderRRef
left join _Document1601 sborka_razborka on sborka_razborka._IDRRef = registr_sebes._RecorderRRef
left join _Document1577 realiazcia on realiazcia._IDRRef = registr_sebes._RecorderRRef
left join _Reference640 partners_analitika on partners_analitika._IDRRef = registr_sebes._Fld92784_RRRef
left join _Reference508 nd_analitika on nd_analitika._IDRRef = registr_sebes._Fld92784_RRRef
left join _Document1527 otvet_hranenie on otvet_hranenie._IDRRef = registr_sebes._RecorderRRef
left join _Document1463 peredacha_hranitel on peredacha_hranitel._IDRRef = registr_sebes._RecorderRRef
left join ( --тут можно поставить left join, чтобы отключить проверку по наличию ГТД в регистре
select
gtd_tovar._Fld40328RRef as id_nomen,
gtd_tovar._Fld40346_RRRef as id_ptu,
LTRIM(RTRIM(gtd._Fld40297)) as gtd_number
from _Document1657 gtd
join _Document1657_VT40325 gtd_tovar on gtd_tovar._Document1657_IDRRef = gtd._IDRRef
where iif(_Posted='',1,0) = 0
) gtds on gtds.id_ptu = registr_sebes._Fld92745_RRRef and gtds.id_nomen = analitik_nomen._Fld53259RRef
left join (select
t1.IDnomen as IDnomen,
t1.Код as Nomen_Code,
t1.[Наименование] as Nomen_name,
t1.[Партийный номер (Сырье и материалы 10 01 ТД)] as Nomen_pn
from (
select *
from (
select
	_Reference539._IDRRef as IDnomen
	,IIF(_Reference539._Marked<>'','Удалено','Не_удалено') as ПометкаУдаления
	,_Reference539._Code as Код
	,_Fld55631 as Артикул
	,_Reference290._Description as ГруппаДоступа
	,_Reference539._Description as Наименование
	,_Reference221._Description as ВидНоменклатуры
	,_Chrc3194._Description as name_
	,_Fld55734_S as value
from dbo._Reference539
join dbo._Reference539_VT55731 on dbo._Reference539_VT55731._Reference539_IDRRef = dbo._Reference539._IDRRef
join dbo._Chrc3194 on dbo._Chrc3194._IDRRef = dbo._Reference539_VT55731._Fld55733RRef
left join dbo._Reference290 on dbo._Reference290._IDRRef = _Fld55642RRef
left join dbo._Reference221 on dbo._Reference221._IDRRef = _Fld55641RRef
left join dbo._InfoRg87665 on dbo._InfoRg87665._Fld87667RRef = dbo._Reference539.[_IDRRef] 
) src
pivot (max([value]) for [name_] in ([Код АСУ НСИ],[Guid КУПОЛ],[Партийный номер (Сырье и материалы 10 01 ТД)],[Тип номенклатуры (Сырье и материалы 10 01 ТД)])) as pvt
)t1
where t1.[Партийный номер (Сырье и материалы 10 01 ТД)] is not null
)nomenklatura on nomenklatura.IDnomen = analitik_nomen._Fld53259RRef
left join _Reference836 seria on analitik_nomen._Fld53261RRef = seria.[_IDRRef]
left join _Reference701 users_ptu on users_ptu._IDRRef = ptu_registr._Fld33129RRef
left join _Reference701 users_spis_registr on users_spis_registr._IDRRef = spis_registr._Fld9185RRef
left join _Reference701 users_vozvrat_tovarov on users_vozvrat_tovarov._IDRRef = vozvrat_tovarov._Fld10003RRef
left join _Reference701 users_peremestit on users_peremestit._IDRRef = peremestit._Fld29148RRef
left join _Reference701 users_storno_spis on users_storno_spis._IDRRef = storno_spis._Fld34602RRef
left join _Reference701 users_peredacha on users_peredacha._IDRRef = peredacha._Fld28475RRef
left join _Reference701 users_vozvrat_siria on users_vozvrat_siria._IDRRef = vozvrat_siria._Fld9631RRef
left join _Reference701 users_sborka_razborka on users_sborka_razborka._IDRRef = sborka_razborka._Fld37175RRef
left join _Reference701 users_realiazcia on users_realiazcia._IDRRef = realiazcia._Fld35985RRef
left join _Reference701 users_otvet_hranenie on users_otvet_hranenie._IDRRef = otvet_hranenie._Fld32303RRef
left join _Reference701 users_peredacha_hranitel on users_peredacha_hranitel._IDRRef = peredacha_hranitel._Fld28723RRef
left join (select
	_IDRRef as _IDRRef
	,_EnumOrder as Порядок
	,Имя
	,Синоним
from dbo._Enum3172
left join (
	select
		417 as N
		,N'ПередачаВЭксплуатацию' as Имя
		,N'Передача в эксплуатацию' as Синоним
) S on S.N=_Enum3172._EnumOrder
) hoz_operacii_spis on hoz_operacii_spis._IDRRef = spis_registr._Fld9173RRef
left join (select
	_IDRRef as _IDRRef
	,_EnumOrder as Порядок
	,Имя
	,Синоним
from dbo._Enum3172
left join (
	select
		0 as N
		,N'АвансовыйОтчет' as Имя
		,N'Авансовый отчет' as Синоним
	union all select
		1 as N
		,N'АмортизацияВнеоборотныхАктивов' as Имя
		,N'Амортизация внеоборотных активов' as Синоним
	union all select
		2 as N
		,N'АмортизацияНМА' as Имя
		,N'Амортизация НМА' as Синоним
	union all select
		3 as N
		,N'АмортизацияНМАвДругуюОрганизацию' as Имя
		,N'Амортизация НМА в другую организацию' as Синоним
	union all select
		4 as N
		,N'АмортизацияНМАизДругойОрганизации' as Имя
		,N'Амортизация НМА из другой организации' as Синоним
	union all select
		5 as N
		,N'АмортизацияОС' as Имя
		,N'Амортизация ОС' as Синоним
	union all select
		6 as N
		,N'АмортизацияОСвДругуюОрганизацию' as Имя
		,N'Амортизация ОС в другую организацию' as Синоним
	union all select
		7 as N
		,N'АмортизацияОСизДругойОрганизации' as Имя
		,N'Амортизация ОС из другой организации' as Синоним
	union all select
		8 as N
		,N'АннулированиеПодарочныхСертификатов' as Имя
		,N'Аннулирование подарочных сертификатов' as Синоним
	union all select
		9 as N
		,N'БронированиеУПоставщика' as Имя
		,N'Бронирование у поставщика' as Синоним
	union all select
		10 as N
		,N'БронированиеЧерезАгента' as Имя
		,N'Бронирование через агента' as Синоним
	union all select
		11 as N
		,N'БронированиеЧерезПодотчетноеЛицо' as Имя
		,N'Бронирование через подотчетное лицо' as Синоним
	union all select
		12 as N
		,N'ВводДанныхПоНалогуНаПрибыль' as Имя
		,N'Ввод данных по налогу на прибыль' as Синоним
	union all select
		13 as N
		,N'ВводИнформацииОПрошлыхРемонтах' as Имя
		,N'Ввод информации о прошлых ремонтах' as Синоним
	union all select
		14 as N
		,N'ВводОстатковАвансовКлиентов' as Имя
		,N'Ввод остатков авансов клиентов' as Синоним
	union all select
		15 as N
		,N'ВводОстатковАвансовПоставщикам' as Имя
		,N'Ввод остатков авансов поставщикам' as Синоним
	union all select
		16 as N
		,N'ВводОстатковАмортизацииНМАиРасходовНаНИОКР' as Имя
		,N'Ввод остатков амортизации НМА и расходов на НИОКР' as Синоним
	union all select
		17 as N
		,N'ВводОстатковАмортизацииОС' as Имя
		,N'Ввод остатков амортизации ОС' as Синоним
	union all select
		18 as N
		,N'ВводОстатковАрендованныхОСЗаБалансом' as Имя
		,N'Ввод остатков арендованных ОС (за балансом)' as Синоним
	union all select
		19 as N
		,N'ВводОстатковАрендованныхОСНаБалансе' as Имя
		,N'Ввод остатков арендованных ОС (на балансе)' as Синоним
	union all select
		20 as N
		,N'ВводОстатковВАвтономныхКассахККМКОформлениюОтчетовОРозничныхПродажах' as Имя
		,N'Ввод остатков в автономных кассах ККМ к оформлению отчетов о розничных продажах' as Синоним
	union all select
		21 as N
		,N'ВводОстатковВАвтономныхКассахККМПоРозничнойВыручке' as Имя
		,N'Ввод остатков в автономных кассах ККМ по розничной выручке' as Синоним
	union all select
		22 as N
		,N'ВводОстатковВзаиморасчетовПоДоговорамАренды' as Имя
		,N'Ввод остатков взаиморасчетов по договорам аренды' as Синоним
	union all select
		23 as N
		,N'ВводОстатковВКассах' as Имя
		,N'Ввод остатков в кассах' as Синоним
	union all select
		24 as N
		,N'ВводОстатковВложенийВоВнеоборотныеАктивы' as Имя
		,N'Ввод остатков вложений во внеоборотные активы' as Синоним
	union all select
		25 as N
		,N'ВводОстатковВозвратнойТарыПереданнойКлиентам' as Имя
		,N'Ввод остатков возвратной тары переданной клиентам' as Синоним
	union all select
		26 as N
		,N'ВводОстатковВозвратнойТарыПринятойОтПоставщиков' as Имя
		,N'Ввод остатков возвратной тары принятой от поставщиков' as Синоним
	union all select
		27 as N
		,N'ВводОстатковДенежныхСредствКПоступлениюОтЭквайера' as Имя
		,N'Ввод остатков денежных средств к поступлению от эквайера' as Синоним
	union all select
		28 as N
		,N'ВводОстатковЗадолженностиКлиентов' as Имя
		,N'Ввод остатков задолженности клиентов' as Синоним
	union all select
		29 as N
		,N'ВводОстатковЗадолженностиПодотчетников' as Имя
		,N'Ввод остатков задолженности подотчетников' as Синоним
	union all select
		30 as N
		,N'ВводОстатковЗадолженностиПоставщикам' as Имя
		,N'Ввод остатков задолженности поставщикам' as Синоним
	union all select
		31 as N
		,N'ВводОстатковЗатратПартийПроизводства' as Имя
		,N'Ввод остатков затрат партий производства' as Синоним
	union all select
		32 as N
		,N'ВводОстатковМатериаловПереданныхВПроизводство' as Имя
		,N'Ввод остатков материалов, переданных в производство' as Синоним
	union all select
		33 as N
		,N'ВводОстатковМатериаловПереданныхПереработчикам' as Имя
		,N'Ввод остатков материалов, переданных переработчикам (2.4)' as Синоним
	union all select
		34 as N
		,N'ВводОстатковМатериаловПереданныхПереработчикам2_5' as Имя
		,N'Ввод остатков материалов, переданных переработчикам' as Синоним
	union all select
		35 as N
		,N'ВводОстатковМатериаловПринятыхВПереработку2_5' as Имя
		,N'Ввод остатков материалов, принятых в переработку' as Синоним
	union all select
		36 as N
		,N'ВводОстатковНаБанковскихСчетах' as Имя
		,N'Ввод остатков на банковских счетах' as Синоним
	union all select
		37 as N
		,N'ВводОстатковНДСПоПриобретеннымЦенностям' as Имя
		,N'Ввод остатков НДС по приобретенным ценностям' as Синоним
	union all select
		38 as N
		,N'ВводОстатковНМАиРасходовНаНИОКР' as Имя
		,N'Ввод остатков нематериальных активов и расходов на НИОКР' as Синоним
	union all select
		39 as N
		,N'ВводОстатковОбесцененияМатериаловПереданныхВПроизводство' as Имя
		,N'Ввод остатков обесценения материалов переданных в производство' as Синоним
	union all select
		40 as N
		,N'ВводОстатковОбесцененияМатериаловПереданныхПереработчикам' as Имя
		,N'Ввод остатков обесценения материалов переданных переработчикам' as Синоним
	union all select
		41 as N
		,N'ВводОстатковОбесцененияНМА' as Имя
		,N'Ввод остатков обесценения НМА' as Синоним
	union all select
		42 as N
		,N'ВводОстатковОбесцененияОС' as Имя
		,N'Ввод остатков обесценения ОС' as Синоним
	union all select
		43 as N
		,N'ВводОстатковОбесцененияСобственныхТоваров' as Имя
		,N'Ввод остатков обесценения собственных товаров' as Синоним
	union all select
		44 as N
		,N'ВводОстатковОбесцененияТоваровПереданныхНаКомиссию' as Имя
		,N'Ввод остатков обесценения товаров переданных на комиссию' as Синоним
	union all select
		45 as N
		,N'ВводОстатковОптовыхПродажЗаПрошлыеПериоды' as Имя
		,N'Ввод остатков оптовых продаж за прошлые периоды' as Синоним
	union all select
		46 as N
		,N'ВводОстатковОсновныхСредств' as Имя
		,N'Ввод остатков основных средств' as Синоним
	union all select
		47 as N
		,N'ВводОстатковПереданныхВАрендуОС' as Имя
		,N'Ввод остатков переданных в аренду основных средств' as Синоним
	union all select
		48 as N
		,N'ВводОстатковПереданныхВАрендуПредметовЛизингаНаБалансе' as Имя
		,N'Ввод остатков переданных в аренду предметов лизинга на балансе' as Синоним
	union all select
		49 as N
		,N'ВводОстатковПерерасходовПодотчетныхСредств' as Имя
		,N'Ввод остатков перерасходов подотчетных средств' as Синоним
	union all select
		50 as N
		,N'ВводОстатковПодарочныхСертификатов' as Имя
		,N'Ввод остатков подарочных сертификатов' as Синоним
	union all select
		51 as N
		,N'ВводОстатковПоДоговорамКредитовИДепозитов' as Имя
		,N'Ввод остатков по договорам кредитов и депозитов' as Синоним
	union all select
		52 as N
		,N'ВводОстатковПолуфабрикатовДавальца2_5' as Имя
		,N'Ввод остатков полуфабрикатов давальца' as Синоним
	union all select
		53 as N
		,N'ВводОстатковПредметовЛизингаЗаБалансом' as Имя
		,N'Ввод остатков предметов лизинга за балансом' as Синоним
	union all select
		54 as N
		,N'ВводОстатковПриПереходеНаИспользованиеАдресногоХраненияОстатков' as Имя
		,N'Ввод остатков при переходе на использование адресного хранения остатков' as Синоним
	union all select
		55 as N
		,N'ВводОстатковПриПереходеНаИспользованиеСкладскихПомещений' as Имя
		,N'Ввод остатков при переходе на использование складских помещений' as Синоним
	union all select
		56 as N
		,N'ВводОстатковПродукцииДавальца2_5' as Имя
		,N'Ввод остатков продукции давальца' as Синоним
	union all select
		57 as N
		,N'ВводОстатковПрочихАктивовПассивов' as Имя
		,N'Ввод остатков прочих активов пассивов' as Синоним
	union all select
		58 as N
		,N'ВводОстатковПрочихРасходов' as Имя
		,N'Ввод остатков прочих расходов' as Синоним
	union all select
		59 as N
		,N'ВводОстатковПрочихРасходовУСН' as Имя
		,N'Ввод остатков прочих расходов УСН' as Синоним
	union all select
		60 as N
		,N'ВводОстатковРасходовУСНПоМатериалам' as Имя
		,N'Ввод остатков расходов УСН по материалам' as Синоним
	union all select
		61 as N
		,N'ВводОстатковРасходовУСНПоТоварам' as Имя
		,N'Ввод остатков расходов УСН по товарам' as Синоним
	union all select
		62 as N
		,N'ВводОстатковРасчетовМеждуОрганизациямиПоАвансам' as Имя
		,N'Ввод остатков расчетов между организациями по авансам' as Синоним
	union all select
		63 as N
		,N'ВводОстатковРасчетовМеждуОрганизациямиПоРеализациям' as Имя
		,N'Ввод остатков расчетов между организациями по реализациям' as Синоним
	union all select
		64 as N
		,N'ВводОстатковРемонтов' as Имя
		,N'Ввод остатков ремонтов' as Синоним
	union all select
		65 as N
		,N'ВводОстатковРозничныхПродажЗаПрошлыеПериоды' as Имя
		,N'Ввод остатков розничных продаж за прошлые периоды' as Синоним
	union all select
		66 as N
		,N'ВводОстатковСобственныхТоваров' as Имя
		,N'Ввод остатков собственных товаров' as Синоним
	union all select
		67 as N
		,N'ВводОстатковСтоимостиНМАиРасходовНаНИОКР' as Имя
		,N'Ввод остатков стоимости НМА и расходов на НИОКР' as Синоним
	union all select
		68 as N
		,N'ВводОстатковСтоимостиОС' as Имя
		,N'Ввод остатков стоимости ОС' as Синоним
	union all select
		69 as N
		,N'ВводОстатковТМЦВЭксплуатации' as Имя
		,N'Ввод остатков ТМЦ в эксплуатации' as Синоним
	union all select
		70 as N
		,N'ВводОстатковТоваровПереданныхНаКомиссию' as Имя
		,N'Ввод остатков товаров, переданных на комиссию' as Синоним
	union all select
		71 as N
		,N'ВводОстатковТоваровПолученныхНаКомиссию' as Имя
		,N'Ввод остатков товаров, полученных на комиссию' as Синоним
	union all select
		72 as N
		,N'ВводОстатковФинансовогоРезультатаЗаПрошлыеПериоды' as Имя
		,N'Ввод остатков финансового результата за прошлые периоды' as Синоним
	union all select
		73 as N
		,N'ВводПервоначальныхСведенийДляРасчетаЗемельногоНалога' as Имя
		,N'Ввод первоначальных сведений для расчета земельного налога' as Синоним
	union all select
		74 as N
		,N'ВводПервоначальныхСведенийДляРасчетаНалогаНаИмущество' as Имя
		,N'Ввод первоначальных сведений для расчета налога на имущество' as Синоним
	union all select
		75 as N
		,N'ВводПервоначальныхСведенийДляРасчетаТранспортногоНалога' as Имя
		,N'Ввод первоначальных сведений для расчета транспортного налога' as Синоним
	union all select
		76 as N
		,N'ВзаимозачетДебиторскойЗадолженности' as Имя
		,N'Взаимозачет дебиторской задолженности' as Синоним
	union all select
		77 as N
		,N'ВзаимозачетЗадолженности' as Имя
		,N'Взаимозачет задолженности' as Синоним
	union all select
		78 as N
		,N'ВзаимозачетКредиторскойЗадолженности' as Имя
		,N'Взаимозачет кредиторской задолженности' as Синоним
	union all select
		79 as N
		,N'ВключениеАмортизационнойПремииВРасходы' as Имя
		,N'Включение амортизационной премии в расходы' as Синоним
	union all select
		80 as N
		,N'ВключениеИсключениеНДСВСтоимости' as Имя
		,N'Включение/исключение НДС в стоимости' as Синоним
	union all select
		81 as N
		,N'ВключениеНДСВСтоимость' as Имя
		,N'Включение НДС в стоимость' as Синоним
	union all select
		82 as N
		,N'ВнесениеДенежныхСредствВКассуККМ' as Имя
		,N'Внесение ДС в кассу ККМ' as Синоним
	union all select
		83 as N
		,N'ВнутреннееПоступлениеДенежныхСредств' as Имя
		,N'Внутреннее поступление ДС' as Синоним
	union all select
		84 as N
		,N'ВнутреннееПоступлениеРабот' as Имя
		,N'Внутреннее поступление работ' as Синоним
	union all select
		85 as N
		,N'ВнутреннееПоступлениеРасходов' as Имя
		,N'Внутреннее поступление расходов' as Синоним
	union all select
		86 as N
		,N'ВнутреннееПоступлениеТоваров' as Имя
		,N'Внутреннее поступление товаров' as Синоним
	union all select
		87 as N
		,N'ВнутреннееПотребление' as Имя
		,N'Внутреннее потребление' as Синоним
	union all select
		88 as N
		,N'ВнутренняяПередачаДенежныхСредств' as Имя
		,N'Передача ДС между организацией и филиалами' as Синоним
	union all select
		89 as N
		,N'ВозвратБронирования' as Имя
		,N'Возврат бронирования' as Синоним
	union all select
		90 as N
		,N'ВозвратБронированияПодотчетногоЛица' as Имя
		,N'Возврат бронирования подотчетного лица' as Синоним
	union all select
		91 as N
		,N'ВозвратВыкупнойСтоимостиПредметовАренды' as Имя
		,N'Возврат выкупной стоимости предметов аренды' as Синоним
	union all select
		92 as N
		,N'ВозвратВыкупнойСтоимостиПредметовАрендыАванс' as Имя
		,N'Возврат выкупной стоимости предметов аренды (аванс)' as Синоним
	union all select
		93 as N
		,N'ВозвратДавальцу' as Имя
		,N'Возврат давальцу (2.4)' as Синоним
	union all select
		94 as N
		,N'ВозвратДавальцу2_5' as Имя
		,N'Возврат давальцу' as Синоним
	union all select
		95 as N
		,N'ВозвратДенежныхДокументовПоставщику' as Имя
		,N'Возврат денежных документов поставщику' as Синоним
	union all select
		96 as N
		,N'ВозвратДенежныхСредствВДругуюОрганизацию' as Имя
		,N'Возврат ДС другой организации' as Синоним
	union all select
		97 as N
		,N'ВозвратДенежныхСредствОтАрендодателя' as Имя
		,N'Возврат ДС от арендодателя' as Синоним
	union all select
		98 as N
		,N'ВозвратДенежныхСредствОтДругойОрганизации' as Имя
		,N'Возврат ДС от другой организации' as Синоним
	union all select
		99 as N
		,N'ВозвратДенежныхСредствОтПодотчетника' as Имя
		,N'Возврат ДС от подотчетника' as Синоним
	union all select
		100 as N
		,N'ВозвратДенежныхСредствОтПоставщика' as Имя
		,N'Возврат ДС от поставщика' as Синоним
	union all select
		101 as N
		,N'ВозвратДеньВДень' as Имя
		,N'Возврат день в день' as Синоним
	union all select
		102 as N
		,N'ВозвратИзПроизводства' as Имя
		,N'Возврат из производства' as Синоним
	union all select
		103 as N
		,N'ВозвратИзЭксплуатации' as Имя
		,N'Возврат из эксплуатации' as Синоним
	union all select
		104 as N
		,N'ВозвратМатериаловИзКладовой' as Имя
		,N'Возврат материалов из кладовой' as Синоним
	union all select
		105 as N
		,N'ВозвратМатериаловИзПроизводства' as Имя
		,N'Возврат материалов из производства' as Синоним
	union all select
		106 as N
		,N'ВозвратНалогов' as Имя
		,N'Возврат налогов' as Синоним
	union all select
		107 as N
		,N'ВозвратНедопоставленногоТовара' as Имя
		,N'Возврат недопоставленного товара' as Синоним
	union all select
		108 as N
		,N'ВозвратНеперечисленнойЗарплатыПоЗарплатномуПроекту' as Имя
		,N'Возврат по зарплатному проекту' as Синоним
	union all select
		109 as N
		,N'ВозвратНеперечисленныхДС' as Имя
		,N'Возврат неперечисленной зарплаты на лицевые счета' as Синоним
	union all select
		110 as N
		,N'ВозвратОбеспечительногоПлатежа' as Имя
		,N'Возврат обеспечительного платежа' as Синоним
	union all select
		111 as N
		,N'ВозвратОплатыКлиенту' as Имя
		,N'Возврат оплаты клиенту' as Синоним
	union all select
		112 as N
		,N'ВозвратОплатыКлиентуНаПлатежнуюКарту' as Имя
		,N'Возврат оплаты клиенту на платежную карту' as Синоним
	union all select
		113 as N
		,N'ВозвратОплатыКомиссионеру' as Имя
		,N'Возврат оплаты комиссионеру' as Синоним
	union all select
		114 as N
		,N'ВозвратОплатыНаПлатежнуюКарту' as Имя
		,N'Возврат оплаты по эквайрингу' as Синоним
	union all select
		115 as N
		,N'ВозвратОСИзАренды' as Имя
		,N'Возврат ОС из аренды' as Синоним
	union all select
		116 as N
		,N'ВозвратОтКомиссионера' as Имя
		,N'Возврат от комиссионера' as Синоним
	union all select
		117 as N
		,N'ВозвратОтПереработчика' as Имя
		,N'Возврат от переработчика (2.4)' as Синоним
	union all select
		118 as N
		,N'ВозвратОтПереработчика2_5' as Имя
		,N'Возврат от переработчика' as Синоним
	union all select
		119 as N
		,N'ВозвратОтРозничногоПокупателя' as Имя
		,N'Возврат от розничного покупателя' as Синоним
	union all select
		120 as N
		,N'ВозвратОтХранителя' as Имя
		,N'Возврат от хранителя' as Синоним
	union all select
		121 as N
		,N'ВозвратПодарочныхСертификатов' as Имя
		,N'Возврат подарочных сертификатов' as Синоним
	union all select
		122 as N
		,N'ВозвратПоКомиссииМеждуОрганизациями' as Имя
		,N'Возврат по комиссии между организациями' as Синоним
	union all select
		123 as N
		,N'ВозвратТарыОтКлиентаПрошлыхПериодов' as Имя
		,N'Возврат тары от клиента прошлых периодов' as Синоним
	union all select
		124 as N
		,N'ВозвратТоваровКомитенту' as Имя
		,N'Возврат товаров комитенту' as Синоним
	union all select
		125 as N
		,N'ВозвратТоваровМеждуОрганизациями' as Имя
		,N'Возврат товаров между организациями' as Синоним
	union all select
		126 as N
		,N'ВозвратТоваровОтКлиента' as Имя
		,N'Возврат товаров от клиента' as Синоним
	union all select
		127 as N
		,N'ВозвратТоваровОтКлиентаПрошлыхПериодов' as Имя
		,N'Возврат товаров от клиента прошлых периодов' as Синоним
	union all select
		128 as N
		,N'ВозвратТоваровПоставщику' as Имя
		,N'Возврат товаров поставщику' as Синоним
	union all select
		129 as N
		,N'ВозвратТоваровЧерезКомиссионера' as Имя
		,N'Возврат товаров через комиссионера' as Синоним
	union all select
		130 as N
		,N'ВозвратТоваровЧерезКомиссионераПрошлыхПериодов' as Имя
		,N'Возврат товаров через комиссионера прошлых периодов' as Синоним
	union all select
		131 as N
		,N'ВосстановлениеАвансаКлиента' as Имя
		,N'Восстановление аванса клиента' as Синоним
	union all select
		132 as N
		,N'ВосстановлениеАвансаПоставщику' as Имя
		,N'Восстановление аванса поставщику' as Синоним
	union all select
		133 as N
		,N'ВосстановлениеАмортизационнойПремии' as Имя
		,N'Восстановление амортизационной премии' as Синоним
	union all select
		134 as N
		,N'ВосстановлениеДолгаКлиента' as Имя
		,N'Восстановление долга клиента' as Синоним
	union all select
		135 as N
		,N'ВосстановлениеДолгаПоставщику' as Имя
		,N'Восстановление долга поставщику' as Синоним
	union all select
		136 as N
		,N'ВосстановлениеНДС' as Имя
		,N'Восстановление НДС' as Синоним
	union all select
		137 as N
		,N'ВосстановлениеНДССВыданногоАванса' as Имя
		,N'Восстановление НДС с выданного аванса' as Синоним
	union all select
		138 as N
		,N'ВосстановлениеОбесцененияНМА' as Имя
		,N'Восстановление обесценения НМА' as Синоним
	union all select
		139 as N
		,N'ВосстановлениеОбесцененияОС' as Имя
		,N'Восстановление обесценения ОС' as Синоним
	union all select
		140 as N
		,N'ВосстановлениеРезервовПоСомнительнымДолгам' as Имя
		,N'Восстановление резервов по сомнительным долгам' as Синоним
	union all select
		141 as N
		,N'ВходящийНДСПоПриобретению' as Имя
		,N'Входящий НДС по приобретению' as Синоним
	union all select
		142 as N
		,N'ВыбытиеАрендованныхОС' as Имя
		,N'Выбытие арендованных ОС (забалансовый учет)' as Синоним
	union all select
		143 as N
		,N'ВыдачаДенежныхДокументовПодотчетнику' as Имя
		,N'Выдача денежных документов подотчетному лицу' as Синоним
	union all select
		144 as N
		,N'ВыдачаДенежныхСредствВДругуюКассу' as Имя
		,N'Выдача ДС в другую кассу' as Синоним
	union all select
		145 as N
		,N'ВыдачаДенежныхСредствВКассуККМ' as Имя
		,N'Выдача ДС в кассу ККМ' as Синоним
	union all select
		146 as N
		,N'ВыдачаДенежныхСредствПодотчетнику' as Имя
		,N'Выдача ДС подотчетнику' as Синоним
	union all select
		147 as N
		,N'ВыдачаЗаймаСотруднику' as Имя
		,N'Выдача займа сотруднику' as Синоним
	union all select
		148 as N
		,N'ВыдачаЗаймов' as Имя
		,N'Выдача займа контрагенту' as Синоним
	union all select
		149 as N
		,N'ВыделениеАмортизацииОСПриРазукомплектации' as Имя
		,N'Выделение амортизации ОС при разукомплектации' as Синоним
	union all select
		150 as N
		,N'ВыделениеСтоимостиОСПриРазукомплектации' as Имя
		,N'Выделение стоимости ОС при разукомплектации' as Синоним
	union all select
		151 as N
		,N'ВыделениеУзловКомпонентовАмортизации' as Имя
		,N'Выделение узлов и компонентов амортизации' as Синоним
	union all select
		152 as N
		,N'ВыемкаДенежныхСредствИзКассыККМ' as Имя
		,N'Выемка ДС из кассы ККМ' as Синоним
	union all select
		153 as N
		,N'ВыкупАрендованныхОС' as Имя
		,N'Выкуп арендованных ОС' as Синоним
	union all select
		154 as N
		,N'ВыкупВозвратнойТарыКлиентом' as Имя
		,N'Выкуп возвратной тары клиентом' as Синоним
	union all select
		155 as N
		,N'ВыкупПринятыхНаХранениеТоваров' as Имя
		,N'Выкуп товаров с хранения' as Синоним
	union all select
		156 as N
		,N'ВыкупТоваровДавальца' as Имя
		,N'Выкуп товаров давальца' as Синоним
	union all select
		157 as N
		,N'ВыкупТоваровПереданныхВПроизводство' as Имя
		,N'Выкуп товаров, переданных в производство' as Синоним
	union all select
		158 as N
		,N'ВыкупТоваровПереданныхНаХранение' as Имя
		,N'Выкуп товаров, переданных на хранение' as Синоним
	union all select
		159 as N
		,N'ВыкупТоваровПереработчиком' as Имя
		,N'Выкуп товаров переработчиком' as Синоним
	union all select
		160 as N
		,N'ВыкупТоваровХранителем' as Имя
		,N'Выкуп товаров хранителем' as Синоним
	union all select
		161 as N
		,N'ВыплатаЗарплаты' as Имя
		,N'Выплата по ведомости' as Синоним
	union all select
		162 as N
		,N'ВыплатаЗарплатыНаЛицевыеСчета' as Имя
		,N'Выплата по ведомости на лицевые счета' as Синоним
	union all select
		163 as N
		,N'ВыплатаЗарплатыПоЗарплатномуПроекту' as Имя
		,N'Выплата по ведомости по зарплатному проекту' as Синоним
	union all select
		164 as N
		,N'ВыплатаЗарплатыРаботнику' as Имя
		,N'Выплата по ведомости работнику' as Синоним
	union all select
		165 as N
		,N'ВыплатаЗарплатыРаздатчиком' as Имя
		,N'Выплата по ведомости раздатчиком' as Синоним
	union all select
		166 as N
		,N'ВыплатаЗарплатыЧерезКассу' as Имя
		,N'Выплата по ведомости через кассу' as Синоним
	union all select
		167 as N
		,N'ВыпускПродукции' as Имя
		,N'Выпуск продукции' as Синоним
	union all select
		168 as N
		,N'ВыпускПродукцииВПодразделение' as Имя
		,N'Выпуск продукции в подразделение' as Синоним
	union all select
		169 as N
		,N'ВыпускПродукцииНаСклад' as Имя
		,N'Выпуск продукции на склад' as Синоним
	union all select
		170 as N
		,N'ВыпускПродукцииПостатейные' as Имя
		,N'Выпуск продукции (постатейные)' as Синоним
	union all select
		171 as N
		,N'ВыпускПродукцииТрудозатраты' as Имя
		,N'Выпуск продукции (трудозатраты)' as Синоним
	union all select
		172 as N
		,N'ВыпускПродукцииФиксированнаяСтоимость' as Имя
		,N'Выпуск продукции (фикс. стоимость)' as Синоним
	union all select
		173 as N
		,N'ВыработкаНМА' as Имя
		,N'Выработка НМА' as Синоним
	union all select
		174 as N
		,N'ВычетНДССВыданногоАванса' as Имя
		,N'Вычет НДС с выданного аванса' as Синоним
	union all select
		175 as N
		,N'ВычетНДССПолученногоАванса' as Имя
		,N'Вычет НДС с полученного аванса' as Синоним
	union all select
		176 as N
		,N'ДвижениеАктивовПассивовЗаСчетАктивовПассивов' as Имя
		,N'Движение активов/пассивов за счет активов/пассивов' as Синоним
	union all select
		177 as N
		,N'ДвижениеДоходовЗаСчетАктивовПассивов' as Имя
		,N'Движение доходов за счет активов/пассивов' as Синоним
	union all select
		178 as N
		,N'ДвижениеДоходовЗаСчетРасходов' as Имя
		,N'Движение доходов за счет расходов' as Синоним
	union all select
		179 as N
		,N'ДвижениеРасходовЗаСчетАктивовПассивов' as Имя
		,N'Движение расходов за счет активов/пассивов' as Синоним
	union all select
		180 as N
		,N'ДвижениеРасходовЗаСчетДоходов' as Имя
		,N'Движение расходов за счет доходов' as Синоним
	union all select
		181 as N
		,N'ДепонированиеЗарплаты' as Имя
		,N'Депонирование зарплаты' as Синоним
	union all select
		182 as N
		,N'ДоначислениеЗемельногоНалога' as Имя
		,N'Доначисление земельного налога' as Синоним
	union all select
		183 as N
		,N'ДоначислениеНалогаНаИмущество' as Имя
		,N'Доначисление налога на имущество' as Синоним
	union all select
		184 as N
		,N'ДоначислениеТранспортногоНалога' as Имя
		,N'Доначисление транспортного налога' as Синоним
	union all select
		185 as N
		,N'ДополнительныеРасходыБезПартии' as Имя
		,N'Дополнительные расходы без указания документа партии' as Синоним
	union all select
		186 as N
		,N'ДополнительныеРасходыСПартией' as Имя
		,N'Дополнительные расходы с указанием документа партии' as Синоним
	union all select
		187 as N
		,N'ДосрочноеПрекращениеДоговораАренды' as Имя
		,N'Досрочное прекращение договора аренды' as Синоним
	union all select
		188 as N
		,N'ДосрочныйВыкупАрендованныхОС' as Имя
		,N'Досрочный выкуп арендованных ОС' as Синоним
	union all select
		189 as N
		,N'ДоходыОтПереоценкиТоваров' as Имя
		,N'Доходы от переоценки товаров' as Синоним
	union all select
		190 as N
		,N'ДоходыПоОтчетуКомиссионераОСписании' as Имя
		,N'Доходы по отчету комиссионера о списании' as Синоним
	union all select
		191 as N
		,N'ЗавершениеЭтаповИсследованийИРазработок' as Имя
		,N'Завершение этапов исследований и разработок' as Синоним
	union all select
		192 as N
		,N'ЗаключениеДоговораАренды' as Имя
		,N'Заключение договора аренды' as Синоним
	union all select
		193 as N
		,N'ЗакрытиеМесяца' as Имя
		,N'Закрытие месяца' as Синоним
	union all select
		194 as N
		,N'ЗакрытиеРасходовОтРеализацииОС' as Имя
		,N'Закрытие расходов от реализации ОС' as Синоним
	union all select
		195 as N
		,N'ЗакрытиеРасходовОтРеализацииОСПослеПереходаПрав' as Имя
		,N'Закрытие расходов от реализации ОС (после перехода прав)' as Синоним
	union all select
		196 as N
		,N'ЗакрытиеРасходовОтРеализацииОССОтложеннымПереходомПрав' as Имя
		,N'Закрытие расходов от реализации ОС (до перехода прав)' as Синоним
	union all select
		197 as N
		,N'ЗакрытиеРасходовОтСписанияОС' as Имя
		,N'Закрытие расходов от списания ОС' as Синоним
	union all select
		198 as N
		,N'ЗакупкаВСтранахЕАЭС' as Имя
		,N'Ввоз из ЕАЭС' as Синоним
	union all select
		199 as N
		,N'ЗакупкаВСтранахЕАЭСНеотфактурованнаяПоставка' as Имя
		,N'Ввоз из ЕАЭС (неотфактурованная поставка)' as Синоним
	union all select
		200 as N
		,N'ЗакупкаВСтранахЕАЭСПоступлениеИзТоваровВПути' as Имя
		,N'Ввоз из ЕАЭС (поступление из товаров в пути)' as Синоним
	union all select
		201 as N
		,N'ЗакупкаВСтранахЕАЭСТоварыВПути' as Имя
		,N'Ввоз из ЕАЭС (товары в пути)' as Синоним
	union all select
		202 as N
		,N'ЗакупкаВСтранахЕАЭСФактуровкаПоставки' as Имя
		,N'Ввоз из ЕАЭС (фактуровка поставки)' as Синоним
	union all select
		203 as N
		,N'ЗакупкаПоИмпорту' as Имя
		,N'Импорт' as Синоним
	union all select
		204 as N
		,N'ЗакупкаПоИмпортуПоступлениеИзТоваровВПути' as Имя
		,N'Импорт (поступление из товаров в пути)' as Синоним
	union all select
		205 as N
		,N'ЗакупкаПоИмпортуТоварыВПути' as Имя
		,N'Импорт (товары в пути)' as Синоним
	union all select
		206 as N
		,N'ЗакупкаУДругойОрганизации' as Имя
		,N'Закупка у другой организации' as Синоним
	union all select
		207 as N
		,N'ЗакупкаУПоставщика' as Имя
		,N'Закупка у поставщика' as Синоним
	union all select
		208 as N
		,N'ЗакупкаУПоставщикаНеотфактурованнаяПоставка' as Имя
		,N'Закупка у поставщика (неотфактурованная поставка)' as Синоним
	union all select
		209 as N
		,N'ЗакупкаУПоставщикаПоступлениеИзТоваровВПути' as Имя
		,N'Закупка у поставщика (поступление из товаров в пути)' as Синоним
	union all select
		210 as N
		,N'ЗакупкаУПоставщикаРеглУчет' as Имя
		,N'Закупка по регл. учету' as Синоним
	union all select
		211 as N
		,N'ЗакупкаУПоставщикаТоварыВПути' as Имя
		,N'Закупка у поставщика (товары в пути)' as Синоним
	union all select
		212 as N
		,N'ЗакупкаУПоставщикаФактуровкаПоставки' as Имя
		,N'Закупка у поставщика (фактуровка поставки)' as Синоним
	union all select
		213 as N
		,N'ЗакупкаЧерезПодотчетноеЛицо' as Имя
		,N'Закупка через подотчетное лицо' as Синоним
	union all select
		214 as N
		,N'ЗаписьКнигиПокупок' as Имя
		,N'Запись книги покупок' as Синоним
	union all select
		215 as N
		,N'ЗачетАвансаВыкупнойСтоимостиВСчетВыкупнойСтоимости' as Имя
		,N'Зачет аванса выкупной стоимости в счет выкупной стоимости' as Синоним
	union all select
		216 as N
		,N'ЗачетАвансаКлиента' as Имя
		,N'Зачет аванса клиента' as Синоним
	union all select
		217 as N
		,N'ЗачетАвансаПоставщику' as Имя
		,N'Зачет аванса поставщику' as Синоним
	union all select
		218 as N
		,N'ЗачетВознагражденияАвансомКомиссионера' as Имя
		,N'Зачет вознаграждения в счет аванса комиссионера' as Синоним
	union all select
		219 as N
		,N'ЗачетВознагражденияАвансомКомитенту' as Имя
		,N'Зачет вознаграждения в счет аванса комитенту' as Синоним
	union all select
		220 as N
		,N'ЗачетВознагражденияОплатойКомиссионера' as Имя
		,N'Зачет вознаграждения оплатой комиссионера' as Синоним
	union all select
		221 as N
		,N'ЗачетВознагражденияОплатойКомитенту' as Имя
		,N'Зачет вознаграждения оплатой комитенту' as Синоним
	union all select
		222 as N
		,N'ЗачетЗемельногоНалога' as Имя
		,N'Зачет земельного налога' as Синоним
	union all select
		223 as N
		,N'ЗачетЗемельногоНалогаВСчетНалогаНаИмущество' as Имя
		,N'Зачет земельного налога в счет налога на имущество' as Синоним
	union all select
		224 as N
		,N'ЗачетЗемельногоНалогаВСчетТранспортногоНалога' as Имя
		,N'Зачет земельного налога в счет транспортного налога' as Синоним
	union all select
		225 as N
		,N'ЗачетНалогаНаИмущество' as Имя
		,N'Зачет налога на имущество' as Синоним
	union all select
		226 as N
		,N'ЗачетНалогаНаИмуществоВСчетЗемельногоНалога' as Имя
		,N'Зачет налога на имущество в счет земельного налога' as Синоним
	union all select
		227 as N
		,N'ЗачетНалогаНаИмуществоВСчетТранспортногоНалога' as Имя
		,N'Зачет налога на имущество в счет транспортного налога' as Синоним
	union all select
		228 as N
		,N'ЗачетОбеспечительногоПлатежаВСчетВыкупнойСтоимости' as Имя
		,N'Зачет обеспечительного платежа в счет выкупной стоимости' as Синоним
	union all select
		229 as N
		,N'ЗачетОплатыУслугиПоАрендеВСчетВыкупнойСтоимости' as Имя
		,N'Зачет оплаты услуги по аренде в счет выкупной стоимости' as Синоним
	union all select
		230 as N
		,N'ЗачетТранспортногоНалога' as Имя
		,N'Зачет транспортного налога' as Синоним
	union all select
		231 as N
		,N'ЗачетТранспортногоНалогаВСчетЗемельногоНалога' as Имя
		,N'Зачет транспортного налога в счет земельного налога' as Синоним
	union all select
		232 as N
		,N'ЗачетТранспортногоНалогаВСчетНалогаНаИмущество' as Имя
		,N'Зачет транспортного налога в счет налога на имущество' as Синоним
	union all select
		233 as N
		,N'ИзлишнеНачисленныеПроцентыПоАренде' as Имя
		,N'Излишне начисленные проценты по аренде' as Синоним
	union all select
		234 as N
		,N'ИзменениеДоходовБудущихПериодовОтЦелевогоФинансированияНМА' as Имя
		,N'Изменение доходов будущих периодов от целевого финансирования НМА' as Синоним
	union all select
		235 as N
		,N'ИзменениеДоходовБудущихПериодовОтЦелевогоФинансированияОС' as Имя
		,N'Изменение доходов будущих периодов от целевого финансирования ОС' as Синоним
	union all select
		236 as N
		,N'ИзменениеПараметровАмортизацииНМА' as Имя
		,N'Изменение параметров амортизации НМА' as Синоним
	union all select
		237 as N
		,N'ИзменениеПараметровАмортизацииОС' as Имя
		,N'Изменение параметров амортизации ОС' as Синоним
	union all select
		238 as N
		,N'ИзменениеПараметровНМА' as Имя
		,N'Изменение параметров НМА' as Синоним
	union all select
		239 as N
		,N'ИзменениеПараметровОС' as Имя
		,N'Изменение параметров ОС' as Синоним
	union all select
		240 as N
		,N'ИзменениеПараметровСтоимостиАрендованногоОС' as Имя
		,N'Изменение параметров стоимости арендованного ОС' as Синоним
	union all select
		241 as N
		,N'ИзменениеПараметровСтоимостиНМА' as Имя
		,N'Изменение параметров стоимости НМА' as Синоним
	union all select
		242 as N
		,N'ИзменениеПараметровСтоимостиОС' as Имя
		,N'Изменение параметров стоимости ОС' as Синоним
	union all select
		243 as N
		,N'ИзменениеСостоянияОС' as Имя
		,N'Изменение состояния ОС' as Синоним
	union all select
		244 as N
		,N'ИзменениеСпособаОтраженияИмущественныхНалогов' as Имя
		,N'Изменение способа отражения имущественных налогов' as Синоним
	union all select
		245 as N
		,N'ИзменениеУсловийДоговораАренды' as Имя
		,N'Изменение условий договора аренды' as Синоним
	union all select
		246 as N
		,N'ИнвентаризационнаяОпись' as Имя
		,N'Инвентаризационная опись' as Синоним
	union all select
		247 as N
		,N'ИнвентаризацияВложенийВОС' as Имя
		,N'Инвентаризация вложений в ОС' as Синоним
	union all select
		248 as N
		,N'ИнвентаризацияКомиссионера' as Имя
		,N'Инвентаризация комиссионера' as Синоним
	union all select
		249 as N
		,N'ИнвентаризацияНезавершенногоСтроительства' as Имя
		,N'Инвентаризация незавершенного строительства' as Синоним
	union all select
		250 as N
		,N'ИнвентаризацияНМА' as Имя
		,N'Инвентаризация НМА' as Синоним
	union all select
		251 as N
		,N'ИнвентаризацияОС' as Имя
		,N'Инвентаризация ОС' as Синоним
	union all select
		252 as N
		,N'ИнвентаризацияТМЦВЭксплуатации' as Имя
		,N'Инвентаризация ТМЦ в эксплуатации' as Синоним
	union all select
		253 as N
		,N'ИнкассацияДенежныхСредствВБанк' as Имя
		,N'Инкассация ДС в банк' as Синоним
	union all select
		254 as N
		,N'ИнкассацияДенежныхСредствИзБанка' as Имя
		,N'Инкассация ДС из банка' as Синоним
	union all select
		255 as N
		,N'ИспользованиеБронированияПодотчетнымЛицом' as Имя
		,N'Использование бронирования подотчетным лицом' as Синоним
	union all select
		256 as N
		,N'ИсправлениеОшибок' as Имя
		,N'Исправление ошибок' as Синоним
	union all select
		257 as N
		,N'ИсправлениеПрочегоНачисленияНДС' as Имя
		,N'Исправление прочего начисления НДС' as Синоним
	union all select
		258 as N
		,N'КомиссияПоЭквайрингу' as Имя
		,N'Комиссия по эквайрингу' as Синоним
	union all select
		259 as N
		,N'КонвертацияВалюты' as Имя
		,N'Конвертация валюты' as Синоним
	union all select
		260 as N
		,N'КонвертацияВалютыПодотчетнымЛицом' as Имя
		,N'Конвертация валюты подотчетным лицом' as Синоним
	union all select
		261 as N
		,N'КорректировкаАрендныхОбязательств' as Имя
		,N'Корректировка арендных обязательств' as Синоним
	union all select
		262 as N
		,N'КорректировкаВидаДеятельностиНДС' as Имя
		,N'Корректировка вида деятельности НДС' as Синоним
	union all select
		263 as N
		,N'КорректировкаДоВводаОстатков' as Имя
		,N'Корректировка до ввода остатков' as Синоним
	union all select
		264 as N
		,N'КорректировкаЗадолженности' as Имя
		,N'Корректировка задолженности' as Синоним
	union all select
		265 as N
		,N'КорректировкаНалогообложенияНДСПартийТоваров' as Имя
		,N'Корректировка налогообложения НДС партий товаров' as Синоним
	union all select
		266 as N
		,N'КорректировкаОбесцененияНМА' as Имя
		,N'Корректировка обесценения НМА' as Синоним
	union all select
		267 as N
		,N'КорректировкаОбесцененияОС' as Имя
		,N'Корректировка обесценения ОС' as Синоним
	union all select
		268 as N
		,N'КорректировкаОбособленногоУчета' as Имя
		,N'Корректировка обособленного учета' as Синоним
	union all select
		269 as N
		,N'КорректировкаОтчетаПереработчика' as Имя
		,N'Корректировка отчета переработчика' as Синоним
	union all select
		270 as N
		,N'КорректировкаПоСогласованиюСторон' as Имя
		,N'Корректировка по согласованию сторон' as Синоним
	union all select
		271 as N
		,N'КорректировкаПриобретенияПрошлогоПериода' as Имя
		,N'Корректировка приобретения прошлого периода' as Синоним
	union all select
		272 as N
		,N'КорректировкаПриобретенияСоСписаниемНаРасходы' as Имя
		,N'Корректировка приобретения со списанием на расходы' as Синоним
	union all select
		273 as N
		,N'КорректировкаПриобретенияСОтражениемНаПрочихДоходах' as Имя
		,N'Корректировка приобретения с отражением на прочих доходах' as Синоним
	union all select
		274 as N
		,N'КорректировкаПриобретенияУвеличениеЗадолженностиСводно' as Имя
		,N'Увеличение задолженности (сводно)' as Синоним
	union all select
		275 as N
		,N'КорректировкаПриобретенияУменьшениеЗадолженностиСводно' as Имя
		,N'Уменьшение задолженности (сводно)' as Синоним
	union all select
		276 as N
		,N'КорректировкаРасходовОтВыбытияОС' as Имя
		,N'Корректировка расходов от выбытия ОС' as Синоним
	union all select
		277 as N
		,N'КорректировкаРеализацииСоСписаниемНаРасходы' as Имя
		,N'Корректировка реализации со списанием на расходы' as Синоним
	union all select
		278 as N
		,N'КорректировкаРеализацииСОтражениемНаПрочихДоходах' as Имя
		,N'Корректировка реализации с отражением на прочих доходах' as Синоним
	union all select
		279 as N
		,N'КорректировкаРеализацииУвеличениеЗадолженностиСводно' as Имя
		,N'Увеличение задолженности (сводно)' as Синоним
	union all select
		280 as N
		,N'КорректировкаРеализацииУменьшениеЗадолженностиСводно' as Имя
		,N'Уменьшение задолженности (сводно)' as Синоним
	union all select
		281 as N
		,N'КорректировкаСтоимостиИАмортизацииНМА' as Имя
		,N'Корректировка стоимости и амортизации НМА' as Синоним
	union all select
		282 as N
		,N'КорректировкаСтоимостиИАмортизацииОС' as Имя
		,N'Корректировка стоимости и амортизации ОС' as Синоним
	union all select
		283 as N
		,N'КорректировкаСтоимостиТМЦОприходованныхПриВыбытииОС' as Имя
		,N'Корректировка стоимости ТМЦ оприходованных при выбытии ОС' as Синоним
	union all select
		284 as N
		,N'КурсовыеРазницыАрендаПрибыль' as Имя
		,N'Курсовые разницы по аренде (прибыль)' as Синоним
	union all select
		285 as N
		,N'КурсовыеРазницыАрендаУбыток' as Имя
		,N'Курсовые разницы по аренде (убыток)' as Синоним
	union all select
		286 as N
		,N'КурсовыеРазницыДепозитыПрибыль' as Имя
		,N'Курсовые разницы по депозитам (прибыль)' as Синоним
	union all select
		287 as N
		,N'КурсовыеРазницыДепозитыУбыток' as Имя
		,N'Курсовые разницы по депозитам (убыток)' as Синоним
	union all select
		288 as N
		,N'КурсовыеРазницыДСПрибыль' as Имя
		,N'Курсовые разницы по денежным средствам (прибыль)' as Синоним
	union all select
		289 as N
		,N'КурсовыеРазницыДСУбыток' as Имя
		,N'Курсовые разницы по денежным средствам (убыток)' as Синоним
	union all select
		290 as N
		,N'КурсовыеРазницыЗаймыВыданныеПрибыль' as Имя
		,N'Курсовые разницы по займам выданным (прибыль)' as Синоним
	union all select
		291 as N
		,N'КурсовыеРазницыЗаймыВыданныеУбыток' as Имя
		,N'Курсовые разницы по займам выданным (убыток)' as Синоним
	union all select
		292 as N
		,N'КурсовыеРазницыКлиентыПрибыль' as Имя
		,N'Курсовые разницы по расчетам с клиентами (прибыль)' as Синоним
	union all select
		293 as N
		,N'КурсовыеРазницыКлиентыУбыток' as Имя
		,N'Курсовые разницы по расчетам с клиентами (убыток)' as Синоним
	union all select
		294 as N
		,N'КурсовыеРазницыКредитыИЗаймыПрибыль' as Имя
		,N'Курсовые разницы по кредитам и займам (прибыль)' as Синоним
	union all select
		295 as N
		,N'КурсовыеРазницыКредитыИЗаймыУбыток' as Имя
		,N'Курсовые разницы по кредитам и займам (убыток)' as Синоним
	union all select
		296 as N
		,N'КурсовыеРазницыПоДисконтированиюПрибыль' as Имя
		,N'Курсовые разницы по дисконтированию (прибыль)' as Синоним
	union all select
		297 as N
		,N'КурсовыеРазницыПоДисконтированиюУбыток' as Имя
		,N'Курсовые разницы по дисконтированию (убыток)' as Синоним
	union all select
		298 as N
		,N'КурсовыеРазницыПоставщикиПрибыль' as Имя
		,N'Курсовые разницы по расчетам с поставщиками (прибыль)' as Синоним
	union all select
		299 as N
		,N'КурсовыеРазницыПоставщикиУбыток' as Имя
		,N'Курсовые разницы по расчетам с поставщиками (убыток)' as Синоним
	union all select
		300 as N
		,N'КурсовыеРазницыРезервыПоДолгамПрибыль' as Имя
		,N'Курсовые разницы резервы по сомнительным долгам (прибыль)' as Синоним
	union all select
		301 as N
		,N'КурсовыеРазницыРезервыПоДолгамУбыток' as Имя
		,N'Курсовые разницы резервы по сомнительным долгам (убыток)' as Синоним
	union all select
		302 as N
		,N'МаркировкаТоваровГИСМ' as Имя
		,N'Маркировка товаров ГИСМ' as Синоним
	union all select
		303 as N
		,N'Модернизация' as Имя
		,N'Модернизация' as Синоним
	union all select
		304 as N
		,N'МодернизацияОС' as Имя
		,N'Модернизация ОС' as Синоним
	union all select
		305 as N
		,N'НаработкаОбъектовЭксплуатации' as Имя
		,N'Наработка объектов эксплуатации' as Синоним
	union all select
		306 as N
		,N'НаработкаТМЦВЭксплуатации' as Имя
		,N'Наработка ТМЦ в эксплуатации' as Синоним
	union all select
		307 as N
		,N'НачислениеВознагражденияЗаСчетРезервов' as Имя
		,N'Начисление вознаграждения за счет резервов' as Синоним
	union all select
		308 as N
		,N'НачислениеДебиторскойЗадолженности' as Имя
		,N'Начисление дебиторской задолженности' as Синоним
	union all select
		309 as N
		,N'НачислениеДивидендов' as Имя
		,N'Начисление дивидендов' as Синоним
	union all select
		310 as N
		,N'НачислениеЗаработнойПлаты' as Имя
		,N'Начисление зарплаты' as Синоним
	union all select
		311 as N
		,N'НачислениеИмущественныхНалогов' as Имя
		,N'Начисление имущественных налогов' as Синоним
	union all select
		312 as N
		,N'НачислениеКредиторскойЗадолженности' as Имя
		,N'Начисление кредиторской задолженности' as Синоним
	union all select
		313 as N
		,N'НачислениеНалогаНаПрибыль' as Имя
		,N'Начисление налога на прибыль' as Синоним
	union all select
		314 as N
		,N'НачислениеНДСВЧастиВыкупнойСтоимости' as Имя
		,N'Начисление НДС в части выкупной стоимости' as Синоним
	union all select
		315 as N
		,N'НачислениеНДСВЧастиОбеспечительногоПлатежа' as Имя
		,N'Начисление НДС в части обеспечительного платежа' as Синоним
	union all select
		316 as N
		,N'НачислениеНДСВЧастиУслугиПоАренде' as Имя
		,N'Начисление НДС в части услуги по аренде' as Синоним
	union all select
		317 as N
		,N'НачислениеНДСНалоговымАгентом' as Имя
		,N'Начисление НДС налоговым агентом' as Синоним
	union all select
		318 as N
		,N'НачислениеНДСпоОтгрузкеТоваровВПути' as Имя
		,N'Начисление НДС по отгрузке без перехода права собственности' as Синоним
	union all select
		319 as N
		,N'НачислениеНДССПолученногоАванса' as Имя
		,N'Начисление НДС с полученного аванса' as Синоним
	union all select
		320 as N
		,N'НачислениеОценочныхОбязательствПоОтпускам' as Имя
		,N'Начисление оценочных обязательств по отпускам' as Синоним
	union all select
		321 as N
		,N'НачислениеПоДоговоруАренды' as Имя
		,N'Начисление по договору аренды' as Синоним
	union all select
		322 as N
		,N'НачислениеПроцентовПоАренде' as Имя
		,N'Начисление процентов по аренде' as Синоним
	union all select
		323 as N
		,N'НачислениеПроцентовПоДисконтированию' as Имя
		,N'Начисление процентов по дисконтированию' as Синоним
	union all select
		324 as N
		,N'НачислениеРеверсивногоНДС' as Имя
		,N'Начисление реверсивного НДС' as Синоним
	union all select
		325 as N
		,N'НачислениеРезерваПодОбесценениеЗапасов' as Имя
		,N'Начисление резерва под обесценение запасов' as Синоним
	union all select
		326 as N
		,N'НачислениеРезервовПоВознаграждениям' as Имя
		,N'Начисление резервов по вознаграждениям' as Синоним
	union all select
		327 as N
		,N'НачислениеРезервовПоСомнительнымДолгам' as Имя
		,N'Начисление резервов по сомнительным долгам' as Синоним
	union all select
		328 as N
		,N'НачислениеРезервовПоСтраховымВзносам' as Имя
		,N'Начисление резервов по страховым взносам' as Синоним
	union all select
		329 as N
		,N'НачислениеРезервовПредстоящихРасходов' as Имя
		,N'Начисление резервов предстоящих расходов' as Синоним
	union all select
		330 as N
		,N'НачислениеСписаниеРезервовПоСомнительнымДолгам' as Имя
		,N'Начисление списание резервов по сомнительным долгам' as Синоним
	union all select
		331 as N
		,N'НачислениеСписаниеРезервовПредстоящихРасходов' as Имя
		,N'Начисление списание резервов предстоящих расходов' as Синоним
	union all select
		332 as N
		,N'НачислениеТорговогоСбора' as Имя
		,N'Начисление торгового сбора' as Синоним
	union all select
		333 as N
		,N'НачисленияПоДепозитам' as Имя
		,N'Начисления по депозитам' as Синоним
	union all select
		334 as N
		,N'НачисленияПоЗаймамВыданным' as Имя
		,N'Начисления по займам выданным' as Синоним
	union all select
		335 as N
		,N'НачисленияПоКредитам' as Имя
		,N'Начисления по кредитам' as Синоним
	union all select
		336 as N
		,N'НедоначисленныеПроцентыПоАренде' as Имя
		,N'Недоначисленные проценты по аренде' as Синоним
	union all select
		337 as N
		,N'ОбеспечительныйПлатеж' as Имя
		,N'Обеспечительный платеж' as Синоним
	union all select
		338 as N
		,N'ОбеспечительныйПлатежПриУчетеЗаБалансом' as Имя
		,N'Обеспечительный платеж при учете за балансом' as Синоним
	union all select
		339 as N
		,N'ОбесценениеНМА' as Имя
		,N'Обесценение НМА' as Синоним
	union all select
		340 as N
		,N'ОбесценениеОС' as Имя
		,N'Обесценение основных средств' as Синоним
	union all select
		341 as N
		,N'ОбъединениеОС' as Имя
		,N'Объединение в новое ОС' as Синоним
	union all select
		342 as N
		,N'ОказаниеАгентскихУслуг' as Имя
		,N'Оказание агентских услуг' as Синоним
	union all select
		343 as N
		,N'ОплатаАрендодателю' as Имя
		,N'Оплата арендодателю' as Синоним
	union all select
		344 as N
		,N'ОплатаВыкупнойСтоимостиПредметовАренды' as Имя
		,N'Оплата выкупной стоимости предметов аренды' as Синоним
	union all select
		345 as N
		,N'ОплатаВыкупнойСтоимостиПредметовАрендыАванс' as Имя
		,N'Оплата выкупной стоимости предметов аренды (аванс)' as Синоним
	union all select
		346 as N
		,N'ОплатаДенежныхСредствВДругуюОрганизацию' as Имя
		,N'Оплата ДС в другую организацию' as Синоним
	union all select
		347 as N
		,N'ОплатаОбеспечительногоПлатежа' as Имя
		,N'Оплата обеспечительного платежа' as Синоним
	union all select
		348 as N
		,N'ОплатаПодарочнымСертификатом' as Имя
		,N'Оплата подарочным сертификатом' as Синоним
	union all select
		349 as N
		,N'ОплатаПоКредитам' as Имя
		,N'Оплата по кредитам и займам полученным' as Синоним
	union all select
		350 as N
		,N'ОплатаПоставщику' as Имя
		,N'Оплата поставщику' as Синоним
	union all select
		351 as N
		,N'ОплатаПоставщикуПодотчетнымЛицом' as Имя
		,N'Оплата поставщику подотчетным лицом' as Синоним
	union all select
		352 as N
		,N'ОплатаПроцентовПоКредитам' as Имя
		,N'Оплата процентов по кредитам' as Синоним
	union all select
		353 as N
		,N'ОплатаУслугПоАренде' as Имя
		,N'Оплата услуг по аренде' as Синоним
	union all select
		354 as N
		,N'ОприходованиеЗаСчетДоходов' as Имя
		,N'Оприходование (за счет доходов/пассивов)' as Синоним
	union all select
		355 as N
		,N'ОприходованиеЗаСчетРасходов' as Имя
		,N'Оприходование (за счет расходов/активов)' as Синоним
	union all select
		356 as N
		,N'ОприходованиеИзлишковТоваровВПользуКомитента' as Имя
		,N'Оприходование излишков товаров в пользу комитента' as Синоним
	union all select
		357 as N
		,N'ОприходованиеИзлишковТоваровВПользуПоклажедателя' as Имя
		,N'Оприходование излишков в пользу поклажедателя' as Синоним
	union all select
		358 as N
		,N'ОприходованиеПоВозврату' as Имя
		,N'Оприходование по возврату' as Синоним
	union all select
		359 as N
		,N'ОприходованиеПриВыбытииОС' as Имя
		,N'Оприходование (при выбытии ОС)' as Синоним
	union all select
		360 as N
		,N'ОприходованиеТМЦВЭксплуатации' as Имя
		,N'Оприходование ТМЦ в эксплуатации' as Синоним
	union all select
		361 as N
		,N'ОприходованиеТоваров' as Имя
		,N'Оприходование товаров' as Синоним
	union all select
		362 as N
		,N'ОтгрузкаБезПереходаПраваСобственности' as Имя
		,N'Отгрузка (товары в пути)' as Синоним
	union all select
		363 as N
		,N'ОтгрузкаПринятыхСПравомПродажиТоваровСХранения' as Имя
		,N'Отгрузка принятых с правом продажи товаров с хранения' as Синоним
	union all select
		364 as N
		,N'ОтклонениеВСтоимостиТоваровДоходы' as Имя
		,N'Отклонение в стоимости товаров (доходы)' as Синоним
	union all select
		365 as N
		,N'ОтклонениеВСтоимостиТоваровРасходы' as Имя
		,N'Отклонение в стоимости товаров (расходы)' as Синоним
	union all select
		366 as N
		,N'ОтклоненияВСтоимостиДенежныхДокументовДоходы' as Имя
		,N'Отклонения в стоимости денежных документов (доходы)' as Синоним
	union all select
		367 as N
		,N'ОтклоненияВСтоимостиДенежныхДокументовРасходы' as Имя
		,N'Отклонения в стоимости денежных документов (расходы)' as Синоним
	union all select
		368 as N
		,N'ОтражениеАрендныхОбязательствВДоходах' as Имя
		,N'Отражение арендных обязательств в доходах' as Синоним
	union all select
		369 as N
		,N'ОтражениеАрендныхОбязательствВРасходах' as Имя
		,N'Отражение арендных обязательств в расходах' as Синоним
	union all select
		370 as N
		,N'ОтражениеВозвратаОплатыЧерезКомиссионера' as Имя
		,N'Отражение возврата оплаты через комиссионера' as Синоним
	union all select
		371 as N
		,N'ОтражениеЗадолженностиПередКомитентом' as Имя
		,N'Отражение задолженности перед комитентом' as Синоним
	union all select
		372 as N
		,N'ОтражениеЗаработнойПлаты' as Имя
		,N'Отражение заработной платы' as Синоним
	union all select
		373 as N
		,N'ОтражениеИзлишкаПриИнвентаризацииДенежныхСредств' as Имя
		,N'Отражение излишка при инвентаризации денежных средств' as Синоним
	union all select
		374 as N
		,N'ОтражениеИзлишкаПриИнкассацииДенежныхСредств' as Имя
		,N'Отражение излишка при инкассации денежных средств' as Синоним
	union all select
		375 as N
		,N'ОтражениеИзлишковНаДоходыПриПоступленииТоваров' as Имя
		,N'Отражение излишков на доходы при поступлении товаров' as Синоним
	union all select
		376 as N
		,N'ОтражениеНалоговВзносовСЗаработнойПлаты' as Имя
		,N'Отражение налогов взносов с заработной платы' as Синоним
	union all select
		377 as N
		,N'ОтражениеНалоговВзносовСоСдельнойЗаработнойПлаты' as Имя
		,N'Отражение налогов взносов со сдельной заработной платы' as Синоним
	union all select
		378 as N
		,N'ОтражениеНДФЛ' as Имя
		,N'Отражение НДФЛ' as Синоним
	union all select
		379 as N
		,N'ОтражениеНедостачЗаСчетПоставщикаПриПоступленииТоваров' as Имя
		,N'Отражение недостач за счет поставщика при поступлении товаров' as Синоним
	union all select
		380 as N
		,N'ОтражениеНедостачЗаСчетСтороннейКомпанииПриПоступленииТоваров' as Имя
		,N'Отражение недостач за счет сторонней компании при поступлении товаров' as Синоним
	union all select
		381 as N
		,N'ОтражениеНедостачиПриИнвентаризацииДенежныхСредств' as Имя
		,N'Отражение недостачи при инвентаризации денежных средств' as Синоним
	union all select
		382 as N
		,N'ОтражениеНедостачиПриИнкассацииДенежныхСредств' as Имя
		,N'Отражение недостачи при инкассации денежных средств' as Синоним
	union all select
		383 as N
		,N'ОтражениеНедостачНаРасходыПриПоступленииТоваров' as Имя
		,N'Отражение недостач на расходы при поступлении товаров' as Синоним
	union all select
		384 as N
		,N'ОтражениеОплатыЧерезКомиссионера' as Имя
		,N'Отражение оплаты через комиссионера' as Синоним
	union all select
		385 as N
		,N'ОтражениеПлановойСтоимостиВыпуска' as Имя
		,N'Отражение плановой стоимости выпуска' as Синоним
	union all select
		386 as N
		,N'ОтражениеПрочихАктивовПассивов' as Имя
		,N'Отражение прочих активов/пассивов' as Синоним
	union all select
		387 as N
		,N'ОтражениеРасходовЗаСчетПрочихАктивовПассивов' as Имя
		,N'Отражение расходов за счет прочих активов/пассивов' as Синоним
	union all select
		388 as N
		,N'ОтражениеСдельнойЗаработнойПлаты' as Имя
		,N'Отражение сдельной заработной платы' as Синоним
	union all select
		389 as N
		,N'ОтражениеУслугПоАрендеВРасходах' as Имя
		,N'Отражение услуг по аренде в расходах' as Синоним
	union all select
		390 as N
		,N'ОтчетБанкаПоОперациямЭквайринга' as Имя
		,N'Отчет банка по операциям эквайринга' as Синоним
	union all select
		391 as N
		,N'ОтчетДавальцу' as Имя
		,N'Отчет давальцу (2.4)' as Синоним
	union all select
		392 as N
		,N'ОтчетДавальцу2_5' as Имя
		,N'Отчет давальцу' as Синоним
	union all select
		393 as N
		,N'ОтчетДавальцуКорректировкаПрошлогоПериода' as Имя
		,N'Отчет давальцу корректировка прошлого периода' as Синоним
	union all select
		394 as N
		,N'ОтчетДавальцуСписаниеНаРасходы' as Имя
		,N'Отчет давальцу (списание на расходы)' as Синоним
	union all select
		395 as N
		,N'ОтчетДавальцуСторно' as Имя
		,N'Отчет давальцу сторно' as Синоним
	union all select
		396 as N
		,N'ОтчетКомиссионера' as Имя
		,N'Отчет комиссионера' as Синоним
	union all select
		397 as N
		,N'ОтчетКомиссионераКомиссия' as Имя
		,N'Отчет комиссионера (комиссионное вознаграждение)' as Синоним
	union all select
		398 as N
		,N'ОтчетКомиссионераОСписании' as Имя
		,N'Отчет комиссионера о списании' as Синоним
	union all select
		399 as N
		,N'ОтчетКомитенту' as Имя
		,N'Отчет комитенту' as Синоним
	union all select
		400 as N
		,N'ОтчетКомитентуКомиссия' as Имя
		,N'Отчет комитенту (комиссионное вознаграждение)' as Синоним
	union all select
		401 as N
		,N'ОтчетКомитентуОСписании' as Имя
		,N'Отчет комитенту о списании' as Синоним
	union all select
		402 as N
		,N'ОтчетПоКомиссииМеждуОрганизациями' as Имя
		,N'Отчет по комиссии между организациями' as Синоним
	union all select
		403 as N
		,N'ОтчетПоКомиссииМеждуОрганизациямиКомиссия' as Имя
		,N'Отчет по комиссии между организациями (комиссионное вознаграждение)' as Синоним
	union all select
		404 as N
		,N'ОтчетПоКомиссииМеждуОрганизациямиОСписании' as Имя
		,N'Отчет по комиссии между организациями о списании' as Синоним
	union all select
		405 as N
		,N'ОтчетПринципалуОЗакупках' as Имя
		,N'Отчет принципалу о закупках' as Синоним
	union all select
		406 as N
		,N'ОтчетПринципалуОЗакупкахКомиссия' as Имя
		,N'Отчет принципалу о закупках (комиссионное вознаграждение)' as Синоним
	union all select
		407 as N
		,N'ОформлениеГТДБрокером' as Имя
		,N'Оформление ГТД через брокера' as Синоним
	union all select
		408 as N
		,N'ОформлениеГТДСамостоятельно' as Имя
		,N'Самостоятельное оформление ГТД' as Синоним
	union all select
		409 as N
		,N'ОформлениеТаможеннойДекларацииЭкспорт' as Имя
		,N'Оформление таможенной декларации на экспорт' as Синоним
	union all select
		410 as N
		,N'ПараметрыНачисленияЗемельногоНалога' as Имя
		,N'Параметры начисления земельного налога' as Синоним
	union all select
		411 as N
		,N'ПараметрыНачисленияНалогаНаИмущество' as Имя
		,N'Параметры начисления налога на имущество' as Синоним
	union all select
		412 as N
		,N'ПараметрыНачисленияТранспортногоНалога' as Имя
		,N'Параметры начисления транспортного налога' as Синоним
	union all select
		413 as N
		,N'ПереводОсновныхСредствИнвестиционногоИмущества' as Имя
		,N'Перевод основных средств и инвестиционного имущества' as Синоним
	union all select
		414 as N
		,N'ПередачаВПроизводство' as Имя
		,N'Передача в производство' as Синоним
	union all select
		415 as N
		,N'ПередачаВСоставНМА' as Имя
		,N'Передача в состав НМА и НИОКР' as Синоним
	union all select
		416 as N
		,N'ПередачаВСоставОС' as Имя
		,N'Передача в состав основных средств' as Синоним
	union all select
		417 as N
		,N'ПередачаВЭксплуатацию' as Имя
		,N'Передача в эксплуатацию' as Синоним
	union all select
		418 as N
		,N'ПередачаВЭксплуатациюБУНУ' as Имя
		,N'Передача в эксплуатацию (БУ и НУ)' as Синоним
	union all select
		419 as N
		,N'ПередачаДавальцу' as Имя
		,N'Передача давальцу (2.4)' as Синоним
	union all select
		420 as N
		,N'ПередачаДавальцу2_5' as Имя
		,N'Передача давальцу' as Синоним
	union all select
		421 as N
		,N'ПередачаМатериаловВКладовую' as Имя
		,N'Передача материалов в кладовую' as Синоним
	union all select
		422 as N
		,N'ПередачаМатериаловВПроизводство' as Имя
		,N'Передача материалов в производство' as Синоним
	union all select
		423 as N
		,N'ПередачаНаКомиссию' as Имя
		,N'Передача на комиссию' as Синоним
	union all select
		424 as N
		,N'ПередачаНаКомиссиюВДругуюОрганизацию' as Имя
		,N'Передача на комиссию в другую организацию' as Синоним
	union all select
		425 as N
		,N'ПередачаНаПрочиеЦели' as Имя
		,N'Передача на прочие цели' as Синоним
	union all select
		426 as N
		,N'ПередачаНаХранениеСПравомПродажи' as Имя
		,N'Передача на хранение с правом продажи' as Синоним
	union all select
		427 as N
		,N'ПередачаОСВАренду' as Имя
		,N'Передача ОС в аренду' as Синоним
	union all select
		428 as N
		,N'ПередачаПереработчику' as Имя
		,N'Передача переработчику (2.4)' as Синоним
	union all select
		429 as N
		,N'ПередачаПереработчику2_5' as Имя
		,N'Передача переработчику' as Синоним
	union all select
		430 as N
		,N'ПередачаПлатежаИзФилиала' as Имя
		,N'Передача платежа из филиала' as Синоним
	union all select
		431 as N
		,N'ПередачаПродукцииИзКладовой' as Имя
		,N'Передача продукции из кладовой' as Синоним
	union all select
		432 as N
		,N'ПередачаПродукцииИзПроизводства' as Имя
		,N'Передача продукции из производства' as Синоним
	union all select
		433 as N
		,N'ПередачаПродукцииИзПроизводстваФиксированнаяСтоимость' as Имя
		,N'Передача продукции из производства (фикс. стоимость)' as Синоним
	union all select
		434 as N
		,N'ПередачаПрочихРасходовМеждуФилиалами' as Имя
		,N'Передача прочих расходов между филиалами' as Синоним
	union all select
		435 as N
		,N'ПеремаркировкаТоваровГИСМ' as Имя
		,N'Перемаркировка товаров ГИСМ' as Синоним
	union all select
		436 as N
		,N'ПеремещениеАмортизацииНМАвДругуюОрганизацию' as Имя
		,N'Перемещение амортизации НМА в другую организацию' as Синоним
	union all select
		437 as N
		,N'ПеремещениеАмортизацииНМАизДругойОрганизации' as Имя
		,N'Перемещение амортизации НМА из другой организации' as Синоним
	union all select
		438 as N
		,N'ПеремещениеАмортизацииОСвДругуюОрганизацию' as Имя
		,N'Перемещение амортизации ОС в другую организацию' as Синоним
	union all select
		439 as N
		,N'ПеремещениеАмортизацииОСизДругойОрганизации' as Имя
		,N'Перемещение амортизации ОС из другой организации' as Синоним
	union all select
		440 as N
		,N'ПеремещениеВЭксплуатации' as Имя
		,N'Перемещение в эксплуатации' as Синоним
	union all select
		441 as N
		,N'ПеремещениеДенежныхДокументов' as Имя
		,N'Перемещение денежных документов' as Синоним
	union all select
		442 as N
		,N'ПеремещениеМатериаловВПроизводстве' as Имя
		,N'Перемещение материалов в производстве' as Синоним
	union all select
		443 as N
		,N'ПеремещениеНМА' as Имя
		,N'Перемещение НМА' as Синоним
	union all select
		444 as N
		,N'ПеремещениеНМАвПодразделениеВыделенноеНаБаланс' as Имя
		,N'Перемещение НМА в подразделение, выделенное на баланс' as Синоним
	union all select
		445 as N
		,N'ПеремещениеОС' as Имя
		,N'Перемещение ОС' as Синоним
	union all select
		446 as N
		,N'ПеремещениеОСвПодразделениеВыделенноеНаБаланс' as Имя
		,N'Перемещение ОС в подразделение, выделенное на баланс' as Синоним
	union all select
		447 as N
		,N'ПеремещениеОСпоИнвентаризации' as Имя
		,N'Перемещение ОС по инвентаризации' as Синоним
	union all select
		448 as N
		,N'ПеремещениеПолуфабрикатов' as Имя
		,N'Перемещение полуфабрикатов' as Синоним
	union all select
		449 as N
		,N'ПеремещениеПолуфабрикатовМеждуФилиалами' as Имя
		,N'Перемещение полуфабрикатов между филиалами' as Синоним
	union all select
		450 as N
		,N'ПеремещениеСтоимостиНМАвДругуюОрганизацию' as Имя
		,N'Перемещение стоимости НМА в другую организацию' as Синоним
	union all select
		451 as N
		,N'ПеремещениеСтоимостиНМАизДругойОрганизации' as Имя
		,N'Перемещение стоимости НМА из другой организации' as Синоним
	union all select
		452 as N
		,N'ПеремещениеСтоимостиОСвДругуюОрганизацию' as Имя
		,N'Перемещение стоимости ОС в другую организацию' as Синоним
	union all select
		453 as N
		,N'ПеремещениеСтоимостиОСизДругойОрганизации' as Имя
		,N'Перемещение стоимости ОС из другой организации' as Синоним
	union all select
		454 as N
		,N'ПеремещениеТоваров' as Имя
		,N'Перемещение товаров' as Синоним
	union all select
		455 as N
		,N'ПеремещениеТоваровМеждуФилиалами' as Имя
		,N'Перемещение товаров между филиалами' as Синоним
	union all select
		456 as N
		,N'ПеремещениеУзлов' as Имя
		,N'Перемещение узлов' as Синоним
	union all select
		457 as N
		,N'ПереносАванса' as Имя
		,N'Перенос аванса' as Синоним
	union all select
		458 as N
		,N'ПереносДолга' as Имя
		,N'Перенос долга' as Синоним
	union all select
		459 as N
		,N'ПереносЗадолженностиМеждуФилиалами' as Имя
		,N'Перенос задолженности между филиалами' as Синоним
	union all select
		460 as N
		,N'ПереносПлатежаМеждуФилиалами' as Имя
		,N'Перенос платежа между филиалами' as Синоним
	union all select
		461 as N
		,N'ПереносПретензииНаАвансы' as Имя
		,N'Перенос претензии на авансы' as Синоним
	union all select
		462 as N
		,N'ПереносПретензииНаРасчеты' as Имя
		,N'Перенос претензии на расчеты' as Синоним
	union all select
		463 as N
		,N'ПереоценкаДенежныхСредств' as Имя
		,N'Переоценка денежных средств' as Синоним
	union all select
		464 as N
		,N'ПереоценкаНМА' as Имя
		,N'Переоценка НМА' as Синоним
	union all select
		465 as N
		,N'ПереоценкаОС' as Имя
		,N'Переоценка ОС' as Синоним
	union all select
		466 as N
		,N'ПереоценкаРасчетовПоАренде' as Имя
		,N'Переоценка расчетов по аренде' as Синоним
	union all select
		467 as N
		,N'ПереоценкаРасчетовСКлиентами' as Имя
		,N'Переоценка расчетов с клиентами' as Синоним
	union all select
		468 as N
		,N'ПереоценкаРасчетовСПоставщиками' as Имя
		,N'Переоценка расчетов с поставщиками' as Синоним
	union all select
		469 as N
		,N'ПереоценкаРезервовПоСомнительнымДолгам' as Имя
		,N'Переоценка резервов по сомнительным долгам' as Синоним
	union all select
		470 as N
		,N'ПереоценкаСуммДисконтирования' as Имя
		,N'Переоценка сумм дисконтирования' as Синоним
	union all select
		471 as N
		,N'ПереоценкаФинансовыхИнструментов' as Имя
		,N'Переоценка финансовых инструментов' as Синоним
	union all select
		472 as N
		,N'ПерерасчетЗемельногоНалога' as Имя
		,N'Перерасчет земельного налога' as Синоним
	union all select
		473 as N
		,N'ПерерасчетИмущественныхНалогов' as Имя
		,N'Перерасчет имущественных налогов' as Синоним
	union all select
		474 as N
		,N'ПерерасчетНалогаНаИмущество' as Имя
		,N'Перерасчет налога на имущество' as Синоним
	union all select
		475 as N
		,N'ПерерасчетТранспортногоНалога' as Имя
		,N'Перерасчет транспортного налога' as Синоним
	union all select
		476 as N
		,N'ПересортицаПартийТоваров' as Имя
		,N'Пересортица партий товаров' as Синоним
	union all select
		477 as N
		,N'ПересортицаТоваров' as Имя
		,N'Пересортица товаров' as Синоним
	union all select
		478 as N
		,N'ПересортицаТоваровСПереоценкой' as Имя
		,N'Пересортица товаров (переоценка)' as Синоним
	union all select
		479 as N
		,N'ПересортицаТоваровУПереработчика' as Имя
		,N'Пересортица товаров у переработчика' as Синоним
	union all select
		480 as N
		,N'ПересортицаТоваровУХранителя' as Имя
		,N'Пересортица товаров у хранителя' as Синоним
	union all select
		481 as N
		,N'ПеречислениеВБюджет' as Имя
		,N'Перечисление налогов и взносов' as Синоним
	union all select
		482 as N
		,N'ПеречислениеДенежныхСредствНаДругойСчет' as Имя
		,N'Перечисление ДС на другой счет' as Синоним
	union all select
		483 as N
		,N'ПеречислениеНаДепозиты' as Имя
		,N'Перечисление на депозиты' as Синоним
	union all select
		484 as N
		,N'ПеречислениеТаможне' as Имя
		,N'Таможенный платеж' as Синоним
	union all select
		485 as N
		,N'ПланированиеПоЗаказуКлиента' as Имя
		,N'Планирование оплаты от клиента' as Синоним
	union all select
		486 as N
		,N'ПланированиеПоЗаказуПоставщику' as Имя
		,N'Планирование оплаты поставщику' as Синоним
	union all select
		487 as N
		,N'ПланированиеПоЗаявке' as Имя
		,N'Планирование по заявке' as Синоним
	union all select
		488 as N
		,N'ПланированиеПоСчету' as Имя
		,N'Планирование по счету' as Синоним
	union all select
		489 as N
		,N'ПогашениеЗадолженностиКлиента' as Имя
		,N'Погашение задолженности клиента' as Синоним
	union all select
		490 as N
		,N'ПогашениеЗадолженностиПоставщику' as Имя
		,N'Погашение задолженности поставщику' as Синоним
	union all select
		491 as N
		,N'ПогашениеЗаймаСотрудником' as Имя
		,N'Погашение займа сотрудником' as Синоним
	union all select
		492 as N
		,N'ПогашениеСтоимостиТМЦВЭксплуатации' as Имя
		,N'Погашение стоимости ТМЦ в эксплуатации' as Синоним
	union all select
		493 as N
		,N'ПодготовкаКПередачеНМА' as Имя
		,N'Подготовка к передаче НМА' as Синоним
	union all select
		494 as N
		,N'ПодготовкаКПередачеОС' as Имя
		,N'Подготовка к передаче ОС' as Синоним
	union all select
		495 as N
		,N'ПокупкаПолученнойВозвратнойТары' as Имя
		,N'Покупка полученной возвратной тары' as Синоним
	union all select
		496 as N
		,N'ПорчаТоваров' as Имя
		,N'Порча товаров' as Синоним
	union all select
		497 as N
		,N'ПорчаТоваровСПереоценкой' as Имя
		,N'Порча товаров с переоценкой' as Синоним
	union all select
		498 as N
		,N'ПорчаТоваровУПереработчика' as Имя
		,N'Порча товаров у переработчика' as Синоним
	union all select
		499 as N
		,N'ПорчаТоваровУХранителя' as Имя
		,N'Порча товаров у хранителя' as Синоним
	union all select
		500 as N
		,N'ПоставкаПодПринципала' as Имя
		,N'Поставка под принципала' as Синоним
	union all select
		501 as N
		,N'ПоступлениеАрендованныхОС' as Имя
		,N'Поступление арендованных ОС (забалансовый учет)' as Синоним
	union all select
		502 as N
		,N'ПоступлениеДенежныхДокументовОтПодотчетника' as Имя
		,N'Поступление денежных документов от подотчетного лица' as Синоним
	union all select
		503 as N
		,N'ПоступлениеДенежныхДокументовОтПоставщика' as Имя
		,N'Поступление денежных документов от поставщика' as Синоним
	union all select
		504 as N
		,N'ПоступлениеДенежныхСредствИзБанка' as Имя
		,N'Поступление ДС из банка' as Синоним
	union all select
		505 as N
		,N'ПоступлениеДенежныхСредствИзДругойКассы' as Имя
		,N'Поступление ДС из другой кассы' as Синоним
	union all select
		506 as N
		,N'ПоступлениеДенежныхСредствИзДругойОрганизации' as Имя
		,N'Поступление ДС от другой организации' as Синоним
	union all select
		507 as N
		,N'ПоступлениеДенежныхСредствИзКассыККМ' as Имя
		,N'Поступление ДС из кассы ККМ' as Синоним
	union all select
		508 as N
		,N'ПоступлениеДенежныхСредствИзКассыНаРасчетныйСчет' as Имя
		,N'Инкассация ДС из кассы на расчетный счет' as Синоним
	union all select
		509 as N
		,N'ПоступлениеДенежныхСредствОтКонвертацииВалюты' as Имя
		,N'Поступление ДС от конвертации валюты' as Синоним
	union all select
		510 as N
		,N'ПоступлениеДенежныхСредствПоДепозитам' as Имя
		,N'Поступление ДС по депозитам' as Синоним
	union all select
		511 as N
		,N'ПоступлениеДенежныхСредствПоЗаймамВыданным' as Имя
		,N'Погашение займа контрагентом' as Синоним
	union all select
		512 as N
		,N'ПоступлениеДенежныхСредствПоКредитам' as Имя
		,N'Поступление по кредитам и займам полученным' as Синоним
	union all select
		513 as N
		,N'ПоступлениеДенежныхСредствСДругогоСчета' as Имя
		,N'Поступление ДС с другого счета' as Синоним
	union all select
		514 as N
		,N'ПоступлениеЗатрат' as Имя
		,N'Поступление затрат' as Синоним
	union all select
		515 as N
		,N'ПоступлениеИзПроизводства' as Имя
		,N'Поступление из производства' as Синоним
	union all select
		516 as N
		,N'ПоступлениеНДСВЧастиВыкупнойСтоимости' as Имя
		,N'Поступление НДС в части выкупной стоимости' as Синоним
	union all select
		517 as N
		,N'ПоступлениеНДСВЧастиОбеспечительногоПлатежа' as Имя
		,N'Поступление НДС в части обеспечительного платежа' as Синоним
	union all select
		518 as N
		,N'ПоступлениеНДСВЧастиУслугиПоАренде' as Имя
		,N'Поступление НДС в части услуги по аренде' as Синоним
	union all select
		519 as N
		,N'ПоступлениеНМА' as Имя
		,N'Поступление НМА и НИОКР' as Синоним
	union all select
		520 as N
		,N'ПоступлениеОбъектовСтроительства' as Имя
		,N'Поступление объектов строительства' as Синоним
	union all select
		521 as N
		,N'ПоступлениеОплатыОтКлиента' as Имя
		,N'Поступление оплаты от клиента' as Синоним
	union all select
		522 as N
		,N'ПоступлениеОплатыОтКлиентаПоПлатежнойКарте' as Имя
		,N'Поступление ДС по эквайринговым операциям' as Синоним
	union all select
		523 as N
		,N'ПоступлениеОплатыПоПлатежнойКарте' as Имя
		,N'Поступление оплаты по эквайрингу' as Синоним
	union all select
		524 as N
		,N'ПоступлениеОС' as Имя
		,N'Поступление основных средств' as Синоним
	union all select
		525 as N
		,N'ПоступлениеОтДавальца' as Имя
		,N'Поступление от давальца (2.4)' as Синоним
	union all select
		526 as N
		,N'ПоступлениеОтДавальца2_5' as Имя
		,N'Поступление от давальца' as Синоним
	union all select
		527 as N
		,N'ПоступлениеОтПереработчика' as Имя
		,N'Поступление от переработчика (2.4)' as Синоним
	union all select
		528 as N
		,N'ПоступлениеОтПереработчика2_5' as Имя
		,N'Поступление от переработчика' as Синоним
	union all select
		529 as N
		,N'ПоступлениеОтПереработчикаФиксированнаяСтоимость' as Имя
		,N'Поступление от переработчика фиксированная стоимость' as Синоним
	union all select
		530 as N
		,N'ПоступлениеПроцентовПоЗаймамВыданным' as Имя
		,N'Поступление процентов по займам выданным' as Синоним
	union all select
		531 as N
		,N'ПоступлениеПрочихАктивов' as Имя
		,N'Поступление прочих активов' as Синоним
	union all select
		532 as N
		,N'ПоступлениеПрочихУслуг' as Имя
		,N'Поступление прочих услуг' as Синоним
	union all select
		533 as N
		,N'ПоступлениеУслуг' as Имя
		,N'Поступление услуг' as Синоним
	union all select
		534 as N
		,N'ПоступлениеУслугДляПроизводства' as Имя
		,N'Поступление услуг для производства' as Синоним
	union all select
		535 as N
		,N'ПоступлениеУслугПоАренде' as Имя
		,N'Поступление услуг по аренде' as Синоним
	union all select
		536 as N
		,N'ПоступлениеУслугРеглУчет' as Имя
		,N'Поступление услуг (закупка по регл.)' as Синоним
	union all select
		537 as N
		,N'ПрекращениеДоговораАренды' as Имя
		,N'Прекращение договора аренды' as Синоним
	union all select
		538 as N
		,N'ПриемкаПодПринципала' as Имя
		,N'Приемка под принципала' as Синоним
	union all select
		539 as N
		,N'ПриемНаКомиссию' as Имя
		,N'Прием на комиссию' as Синоним
	union all select
		540 as N
		,N'ПриемНаХранениеСПравомПродажи' as Имя
		,N'Прием на хранение с правом продажи' as Синоним
	union all select
		541 as N
		,N'ПриемОплатыОтКомиссионера' as Имя
		,N'Прием оплаты от комиссионера' as Синоним
	union all select
		542 as N
		,N'ПриемПередачаРаботМеждуПодразделениями' as Имя
		,N'Прием-передача работ между подразделениями' as Синоним
	union all select
		543 as N
		,N'ПриемПередачаРаботМеждуФилиалами' as Имя
		,N'Прием-передача работ между филиалами' as Синоним
	union all select
		544 as N
		,N'ПриемПлатежаВФилиале' as Имя
		,N'Прием платежа в филиале' as Синоним
	union all select
		545 as N
		,N'ПризнаниеВНУАрендныхПлатежей' as Имя
		,N'Признание в НУ арендных платежей' as Синоним
	union all select
		546 as N
		,N'ПризнаниеРасходовПоИсследованиям' as Имя
		,N'Признание расходов по исследованиям' as Синоним
	union all select
		547 as N
		,N'ПринятиеКУчетуНМА' as Имя
		,N'Принятие к учету НМА' as Синоним
	union all select
		548 as N
		,N'ПринятиеКУчетуНМАпоИнвентаризации' as Имя
		,N'Принятие к учету НМА по инвентаризации' as Синоним
	union all select
		549 as N
		,N'ПринятиеКУчетуОС' as Имя
		,N'Принятие к учету ОС' as Синоним
	union all select
		550 as N
		,N'ПринятиеКУчетуОСпоИнвентаризации' as Имя
		,N'Принятие к учету ОС по инвентаризации' as Синоним
	union all select
		551 as N
		,N'ПринятиеКУчетуПредметовАренды' as Имя
		,N'Принятие к учету предметов аренды' as Синоним
	union all select
		552 as N
		,N'ПринятиеКУчетуСамортизированногоОС' as Имя
		,N'Принятие к учету самортизированного ОС' as Синоним
	union all select
		553 as N
		,N'ПринятиеКУчетуУзловКомпонентовАмортизации' as Имя
		,N'Принятие к учету узлов и компонентов амортизации' as Синоним
	union all select
		554 as N
		,N'ПринятиеНДСкВычету' as Имя
		,N'Принятие НДС к вычету' as Синоним
	union all select
		555 as N
		,N'ПрисоединениеОС' as Имя
		,N'Присоединение к существующему ОС' as Синоним
	union all select
		556 as N
		,N'ПрисоединениеРезервовПоСомнительнымДолгамКДоходам' as Имя
		,N'Присоединение резервов по сомнительным долгам к доходам' as Синоним
	union all select
		557 as N
		,N'ПрисоединениеРезервовПоСомнительнымДолгамКРасходам' as Имя
		,N'Присоединение резервов по сомнительным долгам к расходам' as Синоним
	union all select
		558 as N
		,N'ПроизводствоИзДавальческогоСырья' as Имя
		,N'Производство из давальческого сырья (2.4)' as Синоним
	union all select
		559 as N
		,N'ПроизводствоИзДавальческогоСырья2_5' as Имя
		,N'Производство из давальческого сырья' as Синоним
	union all select
		560 as N
		,N'ПроизводствоУПереработчика' as Имя
		,N'Производство у переработчика (2.4)' as Синоним
	union all select
		561 as N
		,N'ПроизводствоУПереработчика2_5' as Имя
		,N'Производство у переработчика' as Синоним
	union all select
		562 as N
		,N'ПроизводствоУПереработчикаВСтранахЕАЭС2_5' as Имя
		,N'Производство у переработчика (в странах ЕАЭС)' as Синоним
	union all select
		563 as N
		,N'ПрочаяВыдачаДенежныхСредств' as Имя
		,N'Прочий расход ДС' as Синоним
	union all select
		564 as N
		,N'ПрочееНачислениеНДС' as Имя
		,N'Прочее начисление НДС' as Синоним
	union all select
		565 as N
		,N'ПрочееПоступлениеДенежныхСредств' as Имя
		,N'Прочее поступление ДС' as Синоним
	union all select
		566 as N
		,N'ПрочиеДоходы' as Имя
		,N'Прочие доходы' as Синоним
	union all select
		567 as N
		,N'ПрочиеДоходыАктивыПассивы' as Имя
		,N'Прочие доходы за счет прочих активов/пассивов' as Синоним
	union all select
		568 as N
		,N'ПрочиеРасходы' as Имя
		,N'Прочие расходы' as Синоним
	union all select
		569 as N
		,N'ПрочиеРасходыАктивыПассивы' as Имя
		,N'Прочие расходы за счет прочих активов/пассивов' as Синоним
	union all select
		570 as N
		,N'ПрочиеРасходыПодотчетногоЛица' as Имя
		,N'Прочие расходы подотчетного лица' as Синоним
	union all select
		571 as N
		,N'РазборкаТоваров' as Имя
		,N'Разборка на комплектующие' as Синоним
	union all select
		572 as N
		,N'РазукомплектацияОСПолная' as Имя
		,N'Разукомплектация ОС' as Синоним
	union all select
		573 as N
		,N'РазукомплектацияОСЧастичная' as Имя
		,N'Частичная разукомплектация ОС' as Синоним
	union all select
		574 as N
		,N'РаспределениеДоходовПоНаправлениямДеятельности' as Имя
		,N'Распределение доходов по направлениям деятельности' as Синоним
	union all select
		575 as N
		,N'РаспределениеНДС' as Имя
		,N'Распределение НДС' as Синоним
	union all select
		576 as N
		,N'РаспределениеНормируемыхРасходовПоНУ' as Имя
		,N'Распределение нормируемых расходов по НУ' as Синоним
	union all select
		577 as N
		,N'РаспределениеРасходовНаОВЗ' as Имя
		,N'Распределение расходов на объекты возникновения затрат' as Синоним
	union all select
		578 as N
		,N'РаспределениеРасходовНаПартииПроизводства' as Имя
		,N'Распределение расходов на партии производства' as Синоним
	union all select
		579 as N
		,N'РаспределениеРасходовНаСебестоимость' as Имя
		,N'Распределение расходов на себестоимость' as Синоним
	union all select
		580 as N
		,N'РаспределениеРасходовНаСебестоимостьПродаж' as Имя
		,N'Распределение расходов на себестоимость продаж' as Синоним
	union all select
		581 as N
		,N'РаспределениеРасходовНаСебестоимостьПроизводства' as Имя
		,N'Распределение расходов на себестоимость производства' as Синоним
	union all select
		582 as N
		,N'РаспределениеРасходовПоНаправлениямДеятельности' as Имя
		,N'Распределение расходов по направлениям деятельности' as Синоним
	union all select
		583 as N
		,N'РаспределениеРБП' as Имя
		,N'Распределение расходов будущих периодов' as Синоним
	union all select
		584 as N
		,N'РасходыНаТаможенныеСборыШтрафы' as Имя
		,N'Расходы на таможенные сборы (штрафы)' as Синоним
	union all select
		585 as N
		,N'РасходыОтПереоценкиТоваров' as Имя
		,N'Расходы от переоценки товаров' as Синоним
	union all select
		586 as N
		,N'РасходыОтСписанияАктиваСОтложеннымПереходомПрав' as Имя
		,N'Расходы от списания актива с отложенным переходом прав' as Синоним
	union all select
		587 as N
		,N'РасчетРезервовПодОбесценениеЗапасов' as Имя
		,N'Расчет резервов под обесценение запасов' as Синоним
	union all select
		588 as N
		,N'РасчетСебестоимостиТоваров' as Имя
		,N'Расчет себестоимости товаров' as Синоним
	union all select
		589 as N
		,N'РеализацияБезПереходаПраваСобственности' as Имя
		,N'Реализация (товары в пути)' as Синоним
	union all select
		590 as N
		,N'РеализацияВнеоборотныхАктивов' as Имя
		,N'Реализация внеоборотных активов' as Синоним
	union all select
		591 as N
		,N'РеализацияВРозницу' as Имя
		,N'Реализация в розницу' as Синоним
	union all select
		592 as N
		,N'РеализацияКлиенту' as Имя
		,N'Реализация' as Синоним
	union all select
		593 as N
		,N'РеализацияКлиентуРеглУчет' as Имя
		,N'Реализация (только регл. учет)' as Синоним
	union all select
		594 as N
		,N'РеализацияКомиссионногоТовара' as Имя
		,N'Реализация комиссионного товара' as Синоним
	union all select
		595 as N
		,N'РеализацияНМА' as Имя
		,N'Реализация НМА и НИОКР' as Синоним
	union all select
		596 as N
		,N'РеализацияОС' as Имя
		,N'Реализация основных средств' as Синоним
	union all select
		597 as N
		,N'РеализацияОСсОтложеннымПереходомПрав' as Имя
		,N'Реализация ОС с отложенным переходом прав' as Синоним
	union all select
		598 as N
		,N'РеализацияПереданнойВозвратнойТары' as Имя
		,N'Реализация переданной возвратной тары' as Синоним
	union all select
		599 as N
		,N'РеализацияПерепоставленногоТовара' as Имя
		,N'Реализация перепоставленного товара' as Синоним
	union all select
		600 as N
		,N'РеализацияПодарочныхСертификатов' as Имя
		,N'Реализация подарочных сертификатов' as Синоним
	union all select
		601 as N
		,N'РеализацияПрочихАктивов' as Имя
		,N'Реализация прочих активов' as Синоним
	union all select
		602 as N
		,N'РеализацияПрочихУслуг' as Имя
		,N'Реализация прочих услуг' as Синоним
	union all select
		603 as N
		,N'РеализацияТоваровВДругуюОрганизацию' as Имя
		,N'Реализация товаров в другую организацию' as Синоним
	union all select
		604 as N
		,N'РеализацияЧерезКомиссионера' as Имя
		,N'Реализация через комиссионера' as Синоним
	union all select
		605 as N
		,N'РеализацияЧерезКомиссионераБезПереходаПраваСобственности' as Имя
		,N'Реализация через комиссионера (товары в пути)' as Синоним
	union all select
		606 as N
		,N'РегистрацияДефекта' as Имя
		,N'Регистрация дефекта' as Синоним
	union all select
		607 as N
		,N'РегистрацияРасходовУУ' as Имя
		,N'Регистрация расходов в упр. учете' as Синоним
	union all select
		608 as N
		,N'РегистрацияСдельныхРабот' as Имя
		,N'Регистрация сдельных работ' as Синоним
	union all select
		609 as N
		,N'РегламентнаяОперация' as Имя
		,N'Регламентная операция' as Синоним
	union all select
		610 as N
		,N'РегламентнаяОперацияМеждународныйУчет' as Имя
		,N'Регламентная операция международный учет' as Синоним
	union all select
		611 as N
		,N'РезервированиеАвансаКлиента' as Имя
		,N'Резервирование аванса клиента' as Синоним
	union all select
		612 as N
		,N'РеклассификацияДолгосрочныхАктивовОбязательств' as Имя
		,N'Реклассификация долгосрочных активов и обязательств' as Синоним
	union all select
		613 as N
		,N'РеклассификацияДоходов' as Имя
		,N'Реклассификация доходов' as Синоним
	union all select
		614 as N
		,N'РеклассификацияНМА' as Имя
		,N'Реклассификация (изменение параметров) НМА' as Синоним
	union all select
		615 as N
		,N'РеклассификацияОС' as Имя
		,N'Реклассификация (изменение параметров) ОС' as Синоним
	union all select
		616 as N
		,N'РеклассификацияРасходов' as Имя
		,N'Реклассификация расходов' as Синоним
	union all select
		617 as N
		,N'Ремонт' as Имя
		,N'Ремонт' as Синоним
	union all select
		618 as N
		,N'СборкаТоваров' as Имя
		,N'Сборка из комплектующих' as Синоним
	union all select
		619 as N
		,N'СдачаДенежныхСредствВБанк' as Имя
		,N'Сдача ДС в банк' as Синоним
	union all select
		620 as N
		,N'СебестоимостьРеализацииНМА' as Имя
		,N'Себестоимость реализации НМА' as Синоним
	union all select
		621 as N
		,N'СебестоимостьРеализацииОС' as Имя
		,N'Себестоимость реализации ОС' as Синоним
	union all select
		622 as N
		,N'СнятиеНаличныхДенежныхСредств' as Имя
		,N'Инкассация ДС из банка в кассу' as Синоним
	union all select
		623 as N
		,N'СнятиеСРегистрацииЗемельныхУчастков' as Имя
		,N'Снятие с регистрации земельных участков' as Синоним
	union all select
		624 as N
		,N'СнятиеСРегистрацииТранспортныхСредств' as Имя
		,N'Снятие с регистрации транспортных средств' as Синоним
	union all select
		625 as N
		,N'СобственноеПроизводство' as Имя
		,N'Собственное производство' as Синоним
	union all select
		626 as N
		,N'СписаниеАмортизацииНМА' as Имя
		,N'Списание амортизации НМА' as Синоним
	union all select
		627 as N
		,N'СписаниеАмортизацииОС' as Имя
		,N'Списание амортизации ОС' as Синоним
	union all select
		628 as N
		,N'СписаниеБезнадежнойЗадолженностиЗаСчетРезервовПоСомнительнымДолгам' as Имя
		,N'Списание безнадежной задолженности за счет резервов по сомнительным долгам' as Синоним
	union all select
		629 as N
		,N'СписаниеДебиторскойЗадолженности' as Имя
		,N'Списание дебиторской задолженности' as Синоним
	union all select
		630 as N
		,N'СписаниеДебиторскойЗадолженностиНаАктивыПассивы' as Имя
		,N'Списание дебиторской задолженности на активы \ пассивы' as Синоним
	union all select
		631 as N
		,N'СписаниеДебиторскойЗадолженностиНаРасходы' as Имя
		,N'Списание дебиторской задолженности на расходы' as Синоним
	union all select
		632 as N
		,N'СписаниеДенежныхДокументов' as Имя
		,N'Списание денежных документов' as Синоним
	union all select
		633 as N
		,N'СписаниеЗалоговойСтоимостиАрендованныхОС' as Имя
		,N'Списание залоговой стоимости арендованных ОС' as Синоним
	union all select
		634 as N
		,N'СписаниеИзЭксплуатации' as Имя
		,N'Списание из эксплуатации' as Синоним
	union all select
		635 as N
		,N'СписаниеКомиссионныхТоваров' as Имя
		,N'Списание комиссионных товаров' as Синоним
	union all select
		636 as N
		,N'СписаниеКосвенныхРасходов' as Имя
		,N'Списание косвенных расходов' as Синоним
	union all select
		637 as N
		,N'СписаниеКредиторскойЗадолженности' as Имя
		,N'Списание кредиторской задолженности' as Синоним
	union all select
		638 as N
		,N'СписаниеКредиторскойЗадолженностиВДоходы' as Имя
		,N'Списание кредиторской задолженности в доходы' as Синоним
	union all select
		639 as N
		,N'СписаниеНаРасходыМалоценныхТМЦВМесяцеПриобретения' as Имя
		,N'Списание на расходы малоценных ТМЦ в месяце приобретения' as Синоним
	union all select
		640 as N
		,N'СписаниеНаРасходыНИОКР' as Имя
		,N'Списание на расходы НИОКР' as Синоним
	union all select
		641 as N
		,N'СписаниеНаРасходыНИОКРВДругуюОрганизацию' as Имя
		,N'Списание на расходы НИОКР в другую организацию' as Синоним
	union all select
		642 as N
		,N'СписаниеНаРасходыНИОКРИзДругойОрганизации' as Имя
		,N'Списание на расходы НИОКР из другой организации' as Синоним
	union all select
		643 as N
		,N'СписаниеНаРасходыСтоимостиНМАНеПринимаяКУчету' as Имя
		,N'Списание на расходы стоимости НМА (не принимая к учету)' as Синоним
	union all select
		644 as N
		,N'СписаниеНаРасходыСтоимостиОСНеПринимаяКУчету' as Имя
		,N'Списание на расходы стоимости ОС (не принимая к учету)' as Синоним
	union all select
		645 as N
		,N'СписаниеНаРасходыФиксированнаяСтоимость' as Имя
		,N'Списание на расходы (фиксированная стоимость)' as Синоним
	union all select
		646 as N
		,N'СписаниеНДСПоАренде' as Имя
		,N'Списание НДС по аренде' as Синоним
	union all select
		647 as N
		,N'СписаниеНДСПоПриобретеннымЦенностям' as Имя
		,N'Списание НДС по приобретенным ценностям' as Синоним
	union all select
		648 as N
		,N'СписаниеНДССПолученногоАванса' as Имя
		,N'Списание НДС с полученного аванса' as Синоним
	union all select
		649 as N
		,N'СписаниеНедостачЗаСчетКомитента' as Имя
		,N'Списание недостач за счет комитента' as Синоним
	union all select
		650 as N
		,N'СписаниеНедостачЗаСчетПоклажедателя' as Имя
		,N'Списание недостач за счет поклажедателя' as Синоним
	union all select
		651 as N
		,N'СписаниеНеУчитываемойСтоимостиНУ' as Имя
		,N'Списание не учитываемой стоимости НУ' as Синоним
	union all select
		652 as N
		,N'СписаниеНМА' as Имя
		,N'Списание НМА' as Синоним
	union all select
		653 as N
		,N'СписаниеНМАЧастичное' as Имя
		,N'Частичное списание НМА' as Синоним
	union all select
		654 as N
		,N'СписаниеОбесцененияНМА' as Имя
		,N'Списание обесценения НМА' as Синоним
	union all select
		655 as N
		,N'СписаниеОбесцененияОС' as Имя
		,N'Списание обесценения ОС' as Синоним
	union all select
		656 as N
		,N'СписаниеОС' as Имя
		,N'Списание ОС' as Синоним
	union all select
		657 as N
		,N'СписаниеОСпоИнвентаризации' as Имя
		,N'Списание ОС по инвентаризации' as Синоним
	union all select
		658 as N
		,N'СписаниеОСЧастичное' as Имя
		,N'Частичное списание ОС' as Синоним
	union all select
		659 as N
		,N'СписаниеОшибокОкругления' as Имя
		,N'Списание ошибок округления' as Синоним
	union all select
		660 as N
		,N'СписаниеОшибокОкругленияВозвратныеОтходы' as Имя
		,N'Списание ошибок округления (стоимость возвратных отходов в производстве)' as Синоним
	union all select
		661 as N
		,N'СписаниеПринятыхТоваровЗаСчетПоклажедателя' as Имя
		,N'Списание принятых товаров за счет поклажедателя' as Синоним
	union all select
		662 as N
		,N'СписаниеПринятыхТоваровНаРасходы' as Имя
		,N'Списание принятых товаров на расходы' as Синоним
	union all select
		663 as N
		,N'СписаниеПроцентовПоАренде' as Имя
		,N'Списание процентов по аренде' as Синоним
	union all select
		664 as N
		,N'СписаниеПроцентовПоДисконтированию' as Имя
		,N'Списание процентов по дисконтированию' as Синоним
	union all select
		665 as N
		,N'СписаниеПрочихДоходов' as Имя
		,N'Списание прочих доходов' as Синоним
	union all select
		666 as N
		,N'СписаниеПрочихРасходов' as Имя
		,N'Списание прочих расходов' as Синоним
	union all select
		667 as N
		,N'СписаниеРасходовЗаСчетРезервов' as Имя
		,N'Списание расходов за счет резервов' as Синоним
	union all select
		668 as N
		,N'СписаниеРасходовНаПартииПроизводства' as Имя
		,N'Списание расходов на партии производства' as Синоним
	union all select
		669 as N
		,N'СписаниеРезерваПереоценкиАмортизацииНМА' as Имя
		,N'Списание резерва переоценки амортизации НМА' as Синоним
	union all select
		670 as N
		,N'СписаниеРезерваПереоценкиАмортизацииОС' as Имя
		,N'Списание резерва переоценки амортизации ОС' as Синоним
	union all select
		671 as N
		,N'СписаниеРезерваПереоценкиСтоимостиНМА' as Имя
		,N'Списание резерва переоценки стоимости НМА' as Синоним
	union all select
		672 as N
		,N'СписаниеРезерваПереоценкиСтоимостиОС' as Имя
		,N'Списание резерва переоценки стоимости ОС' as Синоним
	union all select
		673 as N
		,N'СписаниеРезервовПодОбесценениеЗапасов' as Имя
		,N'Списание резервов под обесценение запасов' as Синоним
	union all select
		674 as N
		,N'СписаниеРезервовПредстоящихРасходов' as Имя
		,N'Списание резервов предстоящих расходов' as Синоним
	union all select
		675 as N
		,N'СписаниеСтоимостиАрендованныхОС' as Имя
		,N'Списание стоимости арендованных ОС' as Синоним
	union all select
		676 as N
		,N'СписаниеСтоимостиНМА' as Имя
		,N'Списание стоимости НМА' as Синоним
	union all select
		677 as N
		,N'СписаниеСтоимостиОС' as Имя
		,N'Списание стоимости ОС' as Синоним
	union all select
		678 as N
		,N'СписаниеТоваров' as Имя
		,N'Списание товаров' as Синоним
	union all select
		679 as N
		,N'СписаниеТоваровДавальцаЗаСчетДавальца' as Имя
		,N'Списание товаров давальца за счет давальца' as Синоним
	union all select
		680 as N
		,N'СписаниеТоваровДавальцаНаРасходы' as Имя
		,N'Списание товаров давальца на расходы' as Синоним
	union all select
		681 as N
		,N'СписаниеТоваровПоТребованию' as Имя
		,N'Списание на расходы' as Синоним
	union all select
		682 as N
		,N'СписаниеТоваровСХранения' as Имя
		,N'Списание товаров с хранения' as Синоним
	union all select
		683 as N
		,N'СписаниеТоваровУКомиссионера' as Имя
		,N'Списание товаров у комиссионера' as Синоним
	union all select
		684 as N
		,N'СписаниеТоваровУПереработчика' as Имя
		,N'Списание товаров у переработчика' as Синоним
	union all select
		685 as N
		,N'СписаниеУзловКомпонентовАмортизации' as Имя
		,N'Списание узлов и компонентов амортизации' as Синоним
	union all select
		686 as N
		,N'СторнированиеПрочихДоходов' as Имя
		,N'Сторнирование прочих доходов' as Синоним
	union all select
		687 as N
		,N'СторнированиеПрочихРасходов' as Имя
		,N'Сторнирование прочих расходов' as Синоним
	union all select
		688 as N
		,N'СторнированиеРасходовУУ' as Имя
		,N'Сторнирование расходов в упр. учете' as Синоним
	union all select
		689 as N
		,N'СторноОбесцененияНИОКР' as Имя
		,N'Сторно обесценения НИОКР' as Синоним
	union all select
		690 as N
		,N'СторноОбесцененияНИОКРВДругуюОрганизацию' as Имя
		,N'Сторно обесценения НИОКР в другую организацию' as Синоним
	union all select
		691 as N
		,N'СторноОбесцененияНИОКРИзДругойОрганизации' as Имя
		,N'Сторно обесценения НИОКР из другой организации' as Синоним
	union all select
		692 as N
		,N'СторноОбесцененияНМА' as Имя
		,N'Сторно обесценения НМА' as Синоним
	union all select
		693 as N
		,N'СторноОбесцененияНМАВДругуюОрганизацию' as Имя
		,N'Сторно обесценения НМА в другую организацию' as Синоним
	union all select
		694 as N
		,N'СторноОбесцененияНМАИзДругойОрганизации' as Имя
		,N'Сторно обесценения НМА из другой организации' as Синоним
	union all select
		695 as N
		,N'СторноОбесцененияОС' as Имя
		,N'Сторно обесценения ОС' as Синоним
	union all select
		696 as N
		,N'СторноОбесцененияОСВДругуюОрганизацию' as Имя
		,N'Сторно обесценения ОС в другую организацию' as Синоним
	union all select
		697 as N
		,N'СторноОбесцененияОСИзДругойОрганизации' as Имя
		,N'Сторно обесценения ОС из другой организации' as Синоним
	union all select
		698 as N
		,N'СторноПереданнойТары' as Имя
		,N'Сторно переданной тары' as Синоним
	union all select
		699 as N
		,N'СторноПереданнойТарыВозвратНаДругойСклад' as Имя
		,N'Сторно переданной тары (возврат на другой склад)' as Синоним
	union all select
		700 as N
		,N'СторноПоступления' as Имя
		,N'Сторно поступления' as Синоним
	union all select
		701 as N
		,N'СторноПроизводственныхЗатрат' as Имя
		,N'Сторно производственных затрат' as Синоним
	union all select
		702 as N
		,N'СторноРеализации' as Имя
		,N'Сторно реализации' as Синоним
	union all select
		703 as N
		,N'СторноРеализацииВозвратНаДругойСклад' as Имя
		,N'Сторно реализации (возврат на другой склад)' as Синоним
	union all select
		704 as N
		,N'СторноСписанияНаРасходы' as Имя
		,N'Сторно списания на расходы' as Синоним
	union all select
		705 as N
		,N'ТранзитРасходовМеждуОВЗ' as Имя
		,N'Транзит расходов между объектами возникновения затрат' as Синоним
	union all select
		706 as N
		,N'УвеличениеНакопленнойАмортизацииНМА' as Имя
		,N'Увеличение накопленной амортизации НМА' as Синоним
	union all select
		707 as N
		,N'УвеличениеНакопленнойАмортизацииОС' as Имя
		,N'Увеличение накопленной амортизации ОС' as Синоним
	union all select
		708 as N
		,N'УвеличениеНДСПоАренде' as Имя
		,N'Увеличение НДС по аренде' as Синоним
	union all select
		709 as N
		,N'УвеличениеПроцентовПоАренде' as Имя
		,N'Увеличение процентов по аренде' as Синоним
	union all select
		710 as N
		,N'УвеличениеСтоимостиАрендованныхОС' as Имя
		,N'Увеличение стоимости арендованных ОС' as Синоним
	union all select
		711 as N
		,N'УвеличениеСтоимостиНМА' as Имя
		,N'Увеличение стоимости НМА' as Синоним
	union all select
		712 as N
		,N'УвеличениеСтоимостиОС' as Имя
		,N'Увеличение стоимости ОС' as Синоним
	union all select
		713 as N
		,N'УдалитьСписаниеТоваровПереданныхПартнерам' as Имя
		,N'(Не используется) Списание товаров, переданных партнерам' as Синоним
	union all select
		714 as N
		,N'УдержаниеВознагражденияКомиссионера' as Имя
		,N'Удержание вознаграждения комиссионера' as Синоним
	union all select
		715 as N
		,N'УдержаниеВознагражденияКомитентом' as Имя
		,N'Удержание вознаграждения комитентом' as Синоним
	union all select
		716 as N
		,N'УдержаниеИзЗарплатыВСчетРеализацииСотруднику' as Имя
		,N'Удержание из зарплаты в счет реализации сотруднику' as Синоним
	union all select
		717 as N
		,N'УдержаниеИзЗарплатыСотрудника' as Имя
		,N'Удержание из зарплаты сотрудника' as Синоним
	union all select
		718 as N
		,N'УдержаниеНеизрасходованныхПодотчетныхСумм' as Имя
		,N'Удержание неизрасходованных подотчетных сумм' as Синоним
	union all select
		719 as N
		,N'УлучшениеНМА' as Имя
		,N'Улучшение НМА' as Синоним
	union all select
		720 as N
		,N'УменьшениеВеличиныДооценкиНакопленнойАмортизацииНМА' as Имя
		,N'Уменьшение величины дооценки накопленной амортизации НМА' as Синоним
	union all select
		721 as N
		,N'УменьшениеВеличиныДооценкиНакопленнойАмортизацииОС' as Имя
		,N'Уменьшение величины дооценки накопленной амортизации ОС' as Синоним
	union all select
		722 as N
		,N'УменьшениеВеличиныДооценкиСтоимостиНМА' as Имя
		,N'Уменьшение величины дооценки стоимости НМА' as Синоним
	union all select
		723 as N
		,N'УменьшениеВеличиныДооценкиСтоимостиОС' as Имя
		,N'Уменьшение величины дооценки стоимости ОС' as Синоним
	union all select
		724 as N
		,N'УменьшениеНакопленнойАмортизацииНМА' as Имя
		,N'Уменьшение накопленной амортизации НМА' as Синоним
	union all select
		725 as N
		,N'УменьшениеНакопленнойАмортизацииОС' as Имя
		,N'Уменьшение накопленной амортизации ОС' as Синоним
	union all select
		726 as N
		,N'УменьшениеНДСПоАренде' as Имя
		,N'Уменьшение НДС по аренде' as Синоним
	union all select
		727 as N
		,N'УменьшениеПроцентовПоАренде' as Имя
		,N'Уменьшение процентов по аренде' as Синоним
	union all select
		728 as N
		,N'УменьшениеСтоимостиАрендованныхОС' as Имя
		,N'Уменьшение стоимости арендованных ОС' as Синоним
	union all select
		729 as N
		,N'УменьшениеСтоимостиНМА' as Имя
		,N'Уменьшение стоимости НМА' as Синоним
	union all select
		730 as N
		,N'УменьшениеСтоимостиОС' as Имя
		,N'Уменьшение стоимости ОС' as Синоним
	union all select
		731 as N
		,N'УстановкаЗначенийНаработки' as Имя
		,N'Установка значений наработки' as Синоним
	union all select
		732 as N
		,N'ФормированиеСтоимостиАрендованныхОС' as Имя
		,N'Формирование стоимости арендованных ОС' as Синоним
	union all select
		733 as N
		,N'ШтрафыПриВозвратеБронирования' as Имя
		,N'Штрафы при возврате бронирования' as Синоним
	union all select
		734 as N
		,N'ШтрафыПриВозвратеБронированияПодотчетногоЛица' as Имя
		,N'Штрафы при возврате бронирования подотчетного лица' as Синоним
	) S on S.N=_Enum3172._EnumOrder
) hoz_operacii on hoz_operacii._IDRRef = registr_sebes._Fld92775RRef
left join (
select
vtr_potr.[_IDRRef] as DocID,
case 
	when monitor.Elt_bn is not null then monitor.Elt_bn
	when seria.[_Description] != 'Техническая' then seria.[_Description]
	when seria.[_Description] = 'Техническая' then seria.[_Description] 
	else null
end as elt_bn_,
cast(dateadd(year,-2000,vtr_potr.[_Date_Time]) as date) as Period,
vtr_potr.[_Number] as NumberDoc1C,
orderfrom.[_Description] as OrderOut,
nomen.IDnomen,
nomen.Nomen_Code,
nomen.Nomen_pn,
nomen.[Nomen_name] as Nomenklatura,
vtr_potr_tovar.[_LineNo29186] as Item_SO,
vtr_potr_tovar._Fld29191 as Qty_SO,
seria.[_Description] as Seria,
monitor.Elt_bn,
monitor.StatusOperation,
monitor.SO_Number
--objectexpl.[_Description] as ObjectExpl
from _Document1475 vtr_potr
left join _Document1475_VT29185 vtr_potr_tovar on vtr_potr_tovar.[_Document1475_IDRRef] = vtr_potr.[_IDRRef]
left join _Reference848 orderfrom on orderfrom.[_IDRRef] = vtr_potr.[_Fld29152RRef]
left join _Reference836 seria on seria.[_IDRRef] = vtr_potr_tovar.[_Fld29200RRef]
--left join _Reference558 objectexpl on objectexpl.[_IDRRef] = vtr_potr_tovar._Fld9201_RRRef
left join (
select
t1.IDnomen as IDnomen,
t1.Код as Nomen_Code,
t1.[Наименование] as Nomen_name,
t1.[Партийный номер (Сырье и материалы 10 01 ТД)] as Nomen_pn
from (
select *
from (
select
	_Reference539._IDRRef as IDnomen
	,IIF(_Reference539._Marked<>'','Удалено','Не_удалено') as ПометкаУдаления
	,_Reference539._Code as Код
	,_Fld55631 as Артикул
	,_Reference290._Description as ГруппаДоступа
	,_Reference539._Description as Наименование
	,_Reference221._Description as ВидНоменклатуры
	,_Chrc3194._Description as name_
	,_Fld55734_S as value
from dbo._Reference539
join dbo._Reference539_VT55731 on dbo._Reference539_VT55731._Reference539_IDRRef = dbo._Reference539._IDRRef
join dbo._Chrc3194 on dbo._Chrc3194._IDRRef = dbo._Reference539_VT55731._Fld55733RRef
left join dbo._Reference290 on dbo._Reference290._IDRRef = _Fld55642RRef
left join dbo._Reference221 on dbo._Reference221._IDRRef = _Fld55641RRef
left join dbo._InfoRg87665 on dbo._InfoRg87665._Fld87667RRef = dbo._Reference539.[_IDRRef] 
) src
pivot (max([value]) for [name_] in ([Код АСУ НСИ],[Guid КУПОЛ],[Партийный номер (Сырье и материалы 10 01 ТД)],[Тип номенклатуры (Сырье и материалы 10 01 ТД)])) as pvt
)t1
where t1.[Партийный номер (Сырье и материалы 10 01 ТД)] is not null
) nomen on nomen.IDnomen = vtr_potr_tovar.[_Fld29187RRef]
left join (
select
cast(dateadd(year,-2000,monitor.[_Fld96619]) as date) as Period,
RIGHT(monitor.[_Number],(LEN(monitor.[_Number])-CHARINDEX('-',monitor.[_Number],4))) as SO_Number,
status_operation.[_EnumOrder] as StatusOperation,
monitor.[_Fld96623] as TextError,
monitor_tovar.[_Fld96639] as Qty_monitor,
monitor_tovar.[_Fld96646] as Elt_bn,
monitor_tovar.[_LineNo96636] as Item_monitor,
monitor._Fld96622_RRRef as Doc1cId
from _Document96611 monitor
left join (
select
_IDRRef as _IDRRef,
case
	when _EnumOrder = 0 then 'Приемка'
	when _EnumOrder = 1 then 'Размещение'
	when _EnumOrder = 2 then 'Выбытие'
	when _EnumOrder = 3 then 'Перемещение'
	when _EnumOrder = 4 then 'Возврат'
	when _EnumOrder = 5 then 'Заказ'
	when _EnumOrder = 6 then 'Снятие с ВС'
end as _EnumOrder
from _Enum1759
) type_operation on type_operation.[_IDRRef] = monitor._Fld96612RRef
left join (
select
_IDRRef as _IDRRef,
case 
	when _EnumOrder = 0 then 'Загружен'
	when _EnumOrder = 1 then 'В обработке'
	when _EnumOrder = 2 then 'Обработан'
	when _EnumOrder = 3 then 'Отражен в регл. учете'
	when _EnumOrder = 4 then 'Не требует обработки'
	when _EnumOrder = 5 then 'Ошибка'
end as _EnumOrder
from _Enum1781
) status_operation on status_operation.[_IDRRef] = monitor._Fld96621RRef
left join _Document96611_VT96635 monitor_tovar on monitor_tovar.[_Document96611_IDRRef] = monitor.[_IDRRef]
where iif([_Marked]<>'',1,0)=0 and type_operation._EnumOrder = 'Перемещение'
) monitor on monitor.Doc1cId = vtr_potr.[_IDRRef] and monitor.Item_monitor = vtr_potr_tovar.[_LineNo29186]
where iif(vtr_potr._Marked<>'',1,0)=0 and seria.[_Description] is not null
) monitor on monitor.DocID = registr_sebes._RecorderRRef and monitor.IDnomen = nomenklatura.IDnomen and monitor.seria = seria.[_Description]
where cast(dateadd(year,-2000,registr_sebes.[_Period]) as date) >= '2023-03-01' and registr_sebes._Fld92749 not in (0)
and hoz_operacii.Синоним = 'Перемещение товаров'
and seria.[_Description] is not null
and iif(registr_sebes._RecordKind=1,'Списание','Поступление') = 'Списание'
and (case 
	when monitor.elt_bn_ is null then seria.[_Description]
	else monitor.elt_bn_
end) is not null
and hoz_operacii_spis.Имя is null
--and (nomenklatura.Nomen_pn = 'APR05101' or nomenklatura.Nomen_pn = 'BACC30BL6')
--gtd_number = '10005030/220722/3198640' and nomenklatura.Nomen_pn = 'BACS12HM08AH10' and 
--and hoz_operacii.[Синоним] <> 'Перемещение товаров'
group by 
case 
	when ptu_registr._Number is not null then 'Приобретение товаров и услуг ' + ptu_registr._Number
	when spis_registr._Number is not null then 'Списание на расходы ' + spis_registr._Number
 	when vozvrat_tovarov._Number is not null then 'Возврат товаров поставщику ' + vozvrat_tovarov._Number
	when peremestit._Number is not null then 'Перемещение товаров ' + peremestit._Number
	when storno_spis._Number is not null then 'Сторно списания на расходы ' + storno_spis._Number
	when peredacha._Number is not null then 'Передача переработчику ' + peredacha._Number
	when vozvrat_siria._Number is not null then 'Возврат от переработчика ' + vozvrat_siria._Number
	when sborka_razborka._Number is not null then 'Сборка (разборка) товаров ' + sborka_razborka._Number
	when realiazcia._Number is not null then 'Реализация товаров и услуг ' + realiazcia._Number
	when otvet_hranenie._Number is not null then 'Приемка товаров на хранение' + otvet_hranenie._Number
	when peredacha_hranitel._Number is not null then 'Передача на ответ хранение' + peredacha_hranitel._Number
	else registr_sebes._RecorderRRef
end,
case	
	when ptu_registr._Number is not null then 'Приобретение товаров и услуг'
	when spis_registr._Number is not null then 'Списание на расходы'
 	when vozvrat_tovarov._Number is not null then 'Возврат товаров поставщику'
	when peremestit._Number is not null then 'Перемещение товаров'
	when storno_spis._Number is not null then 'Сторно списания на расходы'
	when peredacha._Number is not null then 'Передача переработчику'
	when vozvrat_siria._Number is not null then 'Возврат от переработчика'
	when sborka_razborka._Number is not null then 'Сборка (разборка) товаров'
	when realiazcia._Number is not null then 'Реализация товаров и услуг'
	when otvet_hranenie._Number is not null then 'Приемка товаров на хранение' 
	when peredacha_hranitel._Number is not null then 'Передача на ответ хранение'
	else registr_sebes._RecorderRRef
end,
case 
	when ptu_registr._Number is not null then ptu_registr._Number
	when spis_registr._Number is not null then spis_registr._Number
 	when vozvrat_tovarov._Number is not null then  vozvrat_tovarov._Number
	when peremestit._Number is not null then peremestit._Number
	when storno_spis._Number is not null then storno_spis._Number
	when peredacha._Number is not null then peredacha._Number
	when vozvrat_siria._Number is not null then vozvrat_siria._Number
	when sborka_razborka._Number is not null then sborka_razborka._Number
	when realiazcia._Number is not null then realiazcia._Number
	when otvet_hranenie._Number is not null then otvet_hranenie._Number
	when peredacha_hranitel._Number is not null then peredacha_hranitel._Number
	else registr_sebes._RecorderRRef
end,
gtds.gtd_number,
/*iif(ptu._Number is not null, ptu._Number, 
iif(otvet_hranenie_partia._Number is not null, otvet_hranenie_partia._Number,
registr_sebes._Fld92745_RRRef)),*/
cast(dateadd(year,-2000,registr_sebes._Period) as date),
nomenklatura.Nomen_code,
nomenklatura.Nomen_name,
nomenklatura.Nomen_pn,
monitor.SO_Number,
case 
	when monitor.elt_bn_ is null then seria.[_Description]
	else monitor.elt_bn_
end,
--seria.[_Description],
--monitor.elt_bn_,
--registr_sebes._Fld92749,
--iif(registr_sebes._RecordKind=1,registr_sebes._Fld92749*-1,registr_sebes._Fld92749),
--registr_sebes._Fld92760,
iif(registr_sebes._RecordKind=1,'Списание','Поступление'),
hoz_operacii.[Синоним],
orders._Description,
IIF(object_rashod._Description is not null, object_rashod._Description, 
IIF(partners_analitika._Description is not null, partners_analitika._Description,
IIF(nd_analitika._Description is not null, nd_analitika._Description, 
registr_sebes._Fld92784_RRRef))),
right(IIF(object_rashod._Description is not null, object_rashod._Description, 
IIF(partners_analitika._Description is not null, partners_analitika._Description,
IIF(nd_analitika._Description is not null, nd_analitika._Description, 
registr_sebes._Fld92784_RRRef))),8),
monitor.Item_SO
/*partners._Description,
case 
	when cast(dateadd(year,-2000,registr_sebes._Period) as date) <= '2023-03-13' then 'Дата документа меньше, чем 14.03'
	else null
end,
case 
	when users_ptu._Description is not null then users_ptu._Description
	when users_spis_registr._Description is not null then users_spis_registr._Description
	when users_vozvrat_tovarov._Description is not null then users_vozvrat_tovarov._Description
	when users_peremestit._Description is not null then users_peremestit._Description
	when users_storno_spis._Description is not null then users_storno_spis._Description
	when users_peredacha._Description is not null then users_peredacha._Description
	when users_vozvrat_siria._Description is not null then users_vozvrat_siria._Description
	when users_sborka_razborka._Description is not null then users_sborka_razborka._Description
	when users_realiazcia._Description is not null then users_realiazcia._Description
	when users_otvet_hranenie._Description is not null then users_otvet_hranenie._Description
	when users_peredacha_hranitel._Description is not null then users_peredacha_hranitel._Description
	else null
end*/
order by PN_1C, iif(hoz_operacii.Синоним = 'Передача в состав основных средств',2,iif(hoz_operacii.Синоним='Сторно списания на расходы',1,iif(hoz_operacii.Синоним='Импорт',999,0))), cast(dateadd(year,-2000,registr_sebes._Period) as date) asc
		'''