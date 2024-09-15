from __future__ import annotations
from abc import ABC
# from typing import Callable, Type, TYPE_CHECKING

# from fluent_validation.internal.PropertyRule import PropertyRule


class IIncludeRule(ABC): ...


# class IncludeRule[T](PropertyRule[T, T], IIncludeRule): ...


# 	public IncludeRule(IValidator[T] validator, Func<CascadeMode> cascadeModeThunk, Type typeToValidate)
# 		: base(null, x => x, null, cascadeModeThunk, typeToValidate) {

# 		var adaptor = new ChildValidatorAdaptor[T,T](validator, validator.GetType());
# 		// Note: ChildValidatorAdaptor implements both IPropertyValidator and IAsyncPropertyValidator
# 		// So calling AddAsyncValidator will actually register it as supporting both sync and async.
# 		AddAsyncValidator(adaptor, adaptor);
# 	}

# 	public IncludeRule(Func<ValidationContext[T], T, IValidator[T]> func,  Func<CascadeMode> cascadeModeThunk, Type typeToValidate, Type validatorType)
# 		: base(null, x => x, null, cascadeModeThunk, typeToValidate) {
# 		var adaptor = new ChildValidatorAdaptor<T,T>(func,  validatorType);
# 		// Note: ChildValidatorAdaptor implements both IPropertyValidator and IAsyncPropertyValidator
# 		// So calling AddAsyncValidator will actually register it as supporting both sync and async.
# 		AddAsyncValidator(adaptor, adaptor);
# 	}

# 	public static IncludeRule[T] Create(IValidator[T] validator, Func<CascadeMode> cascadeModeThunk) {
# 		return new IncludeRule[T](validator, cascadeModeThunk, typeof(T));
# 	}

# 	public static IncludeRule[T] Create<TValidator>(Func<T, TValidator> func, Func<CascadeMode> cascadeModeThunk)
# 		where TValidator : IValidator[T] {
# 		return new IncludeRule[T]((ctx, _) => func(ctx.InstanceToValidate), cascadeModeThunk, typeof(T), typeof(TValidator));
# 	}

# 	public override async ValueTask ValidateAsync(ValidationContext[T] context, bool useAsync, CancellationToken cancellation) {
# 		// Special handling for the MemberName selector.
# 		// We need to disable the MemberName selector's cascade functionality whilst executing
# 		// an include rule, as an include rule should be have as if its children are actually children of the parent.
# 		// Also ensure that we only add/remove the state key if it's not present already.
# 		// If it is present already then we're in a situation where there are nested Include rules
# 		// in which case only the root Include rule should add/remove the key.
# 		// See https://github.com/FluentValidation/FluentValidation/issues/1989
# 		bool shouldAddStateKey = !context.RootContextData.ContainsKey(MemberNameValidatorSelector.DisableCascadeKey);

# 		if (shouldAddStateKey) {
# 			context.RootContextData[MemberNameValidatorSelector.DisableCascadeKey] = true;
# 		}

# 		await base.ValidateAsync(context, useAsync, cancellation);

# 		if (shouldAddStateKey) {
# 			context.RootContextData.Remove(MemberNameValidatorSelector.DisableCascadeKey);
# 		}
# 	}
# }
